import os

from typing import Any, Dict, List, Optional, Tuple
from langchain.chains.graph_qa.cypher import extract_cypher
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, PromptTemplate

from langchain.chains import GraphCypherQAChain
from langchain.callbacks.manager import CallbackManagerForChainRun

try:
    from pydantic.v1.main import BaseModel, Field
except ImportError:
    from pydantic.main import BaseModel, Field

from cypher_validator import CypherQueryCorrector, Schema


def remove_entities(doc):
    """
    Replace named entities in the given text with their corresponding entity labels.

    Parameters:
    - doc (Spacy Document): processed SpaCy document of the input text.

    Returns:
    - str: The modified text with named entities replaced by their entity labels.

    Example:
    >>> replace_entities_with_labels("Apple is looking at buying U.K. startup for $1 billion.")
    'ORG is looking at buying GPE startup for MONEY .'
    """
    # Initialize an empty list to store the new tokens
    new_tokens = []
    # Keep track of the end index of the last entity
    last_end = 0

    # Iterate through entities, replacing them with their entity label
    for ent in doc.ents:
        # Add the tokens that come before this entity
        new_tokens.extend([token.text for token in doc[last_end : ent.start]])
        # Replace the entity with its label
        new_tokens.append(f"{ent.label_}")
        # Update the last entity end index
        last_end = ent.end

    # Add any remaining tokens after the last entity
    new_tokens.extend([token.text for token in doc[last_end:]])
    # Join the new tokens into a single string
    new_text = " ".join(new_tokens)
    return new_text


AVAILABLE_RELATIONSHIPS = [
    Schema("Person", "HAS_PARENT", "Person"),
    Schema("Person", "HAS_CHILD", "Person"),
    Schema("Organization", "HAS_SUPPLIER", "Organization"),
    Schema("Organization", "IN_CITY", "City"),
    Schema("Organization", "HAS_CATEGORY", "IndustryCategory"),
    Schema("Organization", "HAS_CEO", "Person"),
    Schema("Organization", "HAS_SUBSIDIARY", "Organization"),
    Schema("Organization", "HAS_COMPETITOR", "Organization"),
    Schema("Organization", "HAS_BOARD_MEMBER", "Person"),
    Schema("Organization", "HAS_INVESTOR", "Organization"),
    Schema("Organization", "HAS_INVESTOR", "Person"),
    Schema("City", "IN_COUNTRY", "Country"),
    Schema("Article", "HAS_CHUNK", "Chunk"),
    Schema("Article", "MENTIONS", "Organization")
]

CYPHER_SYSTEM_TEMPLATE = """
Purpose:
Your role is to convert user questions concerning data in a Neo4j database into accurate Cypher queries.
"""

cypher_query_corrector = CypherQueryCorrector(AVAILABLE_RELATIONSHIPS)

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.
Even if the question doesn't provide full person or organization names, you should use the full names from the provided
information to construct an answer.
Information:
{context}

Question: {question}
Helpful Answer:"""
CYPHER_QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)


class Entities(BaseModel):
    """Identifying information about entities."""

    name: List[str] = Field(
        ...,
        description="All the person, organization, or business entities that appear in the text",
    )


class CustomCypherChain(GraphCypherQAChain):
    def process_entities(self, text: str) -> List[str]:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are extracting organization and person entities from the text.",
                ),
                (
                    "human",
                    "Use the given format to extract information from the following input: {input}",
                ),
            ]
        )

        entity_chain = create_structured_output_chain(
            Entities, self.qa_chain.llm, prompt
        )
        entities = entity_chain.run(text)
        print(entities)
        return entities.name

    def get_viz_data(self, entities: List[str]) -> List[Tuple[str, str]]:
        viz_query = """
        MATCH (n:Person|Organization) WHERE n.name IN $entities
        CALL {
            WITH n
            MATCH (n)-[r:!MENTIONS]->(m)
            WHERE m.name IS NOT NULL
            RETURN n.name AS source, type(r) AS type, m.name AS target
            LIMIT 5
            UNION
            WITH n
            MATCH (n)<-[r:!MENTIONS]-(m)
            WHERE m.name IS NOT NULL
            RETURN n.name AS target, type(r) AS type, m.name AS source
            LIMIT 5
        }
        RETURN source, type, target LIMIT 20
        """
        results = self.graph.query(viz_query, {"entities": entities})
        return results

    def find_entity_match(self, entity: str, k: int = 3) -> List[str]:
        fts_query = """
        CALL db.index.fulltext.queryNodes('entity', $entity + "*", {limit:$k})
        YIELD node,score
        RETURN node.name AS result
        """

        return [
            el["result"]
            for el in self.graph.query(
                fts_query, {"entity": "AND ".join(entity.split()), "k": k}
            )
        ]

    def generate_system_message(
        self, relevant_entities: str = "", fewshot_examples: str = ""
    ) -> SystemMessage:
        system_message = CYPHER_SYSTEM_TEMPLATE
        system_message += (
            f"Database Schema: Please refer to the provided database schema {self.graph_schema} for reference. "
            "Guidelines: Relationships & Properties: Utilize only the relationship types "
            "and properties specified in the provided schema. Do not introduce new ones.\n"
        )
        if relevant_entities:
            system_message += (
                f"Entity Substitution: If the question mentions specific entities, replace them in the query with corresponding entities from "
                f"the given list. Given list of entities is: {relevant_entities}\n"
                "Example: If the list contains John: ['John Goodman'], replace 'John' in the query with 'John Goodman'."
                "Flexible Queries: Ensure your Cypher queries can capture all relevant entities.\n"
                "Correct: MATCH (p:Person) WHERE p.name IN ['John Goodman', 'John Stockton'] MATCH (p)<-[:BOARD_MEMBER]-(o:Organization)"
            )
        if fewshot_examples:
            system_message += (
                f"Example Queries: Please refer to the provided example queries for constructing Cypher statements:\n"
                f"{fewshot_examples}\n"
            )

        system_message += (
            "Informative Responses: Ensure your responses contain sufficient information to answer the question for anyone lacking context.\n"
            "Include details about both persons and organizations, if applicable. \n"
            "Text Search: To search text, avoid using the CONTAINS clause. "
            "Instead, employ apoc.ml.openai.embedding and gds.similarity.cosine functions or db.index.vector.queryNodes.\n"
            "Note: If you use apoc.ml.openai.embedding, it must be the first operation in your query.\n"
            "Result Chunking: When returning text, always provide exactly three chunks—no more, no less.\n"
            "By following these guidelines, you'll ensure the generated Cypher queries accurately reflect the database entities and relationships."
            "Solve it step by step."
        )
        return SystemMessage(content=system_message)

    def get_fewshot_examples(self, question):
        results = self.graph.query(
            """
        CALL apoc.ml.openai.embedding([$question], $openai_api_key)
                                    YIELD embedding                             
        CALL db.index.vector.queryNodes('fewshot', 3, embedding)
                                    YIELD node, score
        RETURN node.Question AS question, node.Cypher as cypher
                                    """,
            {"question": question, "openai_api_key": os.environ["OPENAI_API_KEY"]},
        )

        fewshot = "\n".join([f"#{el['question']}\n{el['cypher']}" for el in results])
        print("-" * 30)
        print(fewshot)
        return fewshot

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:

        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        question = inputs[self.input_key]
        chat_history = inputs["chat_history"]
        # Extract mentioned people and organizations and match them to database values
        entities = self.process_entities(question)
        print(f"NER found: {entities}")
        relevant_entities = dict()
        for entity in entities:
            relevant_entities[entity] = self.find_entity_match(entity)
        print(f"Relevant entities are: {relevant_entities}")

        # Get few-shot examples using vector search
        fewshots = self.get_fewshot_examples(question)

        system = self.generate_system_message(str(relevant_entities), fewshots)
        generated_cypher = self.cypher_generation_chain.llm.predict_messages(
            [system] + chat_history
        )
        print(generated_cypher.content)
        generated_cypher = extract_cypher(generated_cypher.content)
        validated_cypher = cypher_query_corrector(
            generated_cypher
        )
        print(validated_cypher)
        # If Cypher statement wasn't generated
        # Usually happens when LLM decides it can't answer
        if not "RETURN" in validated_cypher:
            chain_result: Dict[str, Any] = {
                self.output_key: validated_cypher,
                "viz_data": (None, None),
                "database": None,
                "cypher": None,
            }
            return chain_result

        # Retrieve and limit the number of results
        context = self.graph.query(
            validated_cypher, {"openai_api_key": os.environ["OPENAI_API_KEY"]}
        )[: self.top_k]

        result = self.qa_chain(
            {"question": question, "context": context}, callbacks=callbacks
        )
        final_result = result[self.qa_chain.output_key]

        final_entities = self.process_entities(final_result)
        if final_entities:
            viz_data = self.get_viz_data(final_entities)
        else:
            viz_data = None

        chain_result: Dict[str, Any] = {
            self.output_key: final_result,
            "viz_data": (viz_data, final_entities),
            "database": context,
            "cypher": validated_cypher,
        }
        return chain_result
