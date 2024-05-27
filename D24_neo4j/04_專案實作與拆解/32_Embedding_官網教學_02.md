# 官網教學

[Part 1](https://www.mongodb.com/developer/products/atlas/choose-embedding-model-rag/)

[Part 2](https://www.mongodb.com/developer/products/atlas/evaluate-llm-applications-rag/)

_以下官方教程從安裝必要的工具開始，接著設置與連線數據庫、使用 API 密鑰、下載和處理數據集、生成嵌入並存儲到 MongoDB 中，然後使用這些 `嵌入` 來進行 `檢索和生成，最後評估整體系統的性能並追蹤變化。這些步驟確保了我們能夠高效地評估和改進我們的 LLM 應用。_

<br>

## 說明

1. 安裝所需的庫：參數 `-q` 是 `安靜模式`，減少無謂的訊息輸出；參數 `-U` 是自動更新已安裝的套件。

    ```python
    pip install -qU toml datasets ragas langchain langchain-mongodb langchain-openai pymongo pandas tqdm matplotlib seaborn
    ```

   - `datasets`：從 Hugging Face Hub 獲取數據集。

   - `ragas`：RAGAS 框架，用於評估 RAG 應用。

   - `langchain`：用於開發 LLM 應用。

   - `langchain-mongodb`：用於將 MongoDB Atlas 作為向量存儲使用。

   - `langchain-openai`：用於在 LangChain 中使用 OpenAI 模型。

   - `pymongo`：用於與 MongoDB 交互的 Python 驅動。

   - `pandas`：用於數據分析、探索和操作。

   - `tdqm`：顯示進度條。

   - `matplotlib` 和 `seaborn`：用於數據可視化。

<br>

2. 設置先決條件：設置 `MongoDB Atlas` 作為 `向量存儲` ，建立資料庫與集合，並取得連線的 `URI`，記得將主機 IP 加入可訪問列表中。

<br>

## 撰寫代碼

1. 設置敏感資訊處理模式：官網使用 `getpass`，這裡我改用 `toml`。

    ```python
    # import getpass
    import toml

    # MongoDB URI
    ATLAS_CONNECTION_STRING = toml.load("MONGODB_URL")
    ```

<br>

2. 在腳本同層級目錄新建存放密鑰的敏感茲訓的腳本 `secrets.toml`，_特別注意_，要觀察一下 `.gitignore` 文件中是否已經寫入 `secrets.toml` 或 `**/secrets.toml`，並且記得替換自己的密碼。

    ```bash
    MONGODB_URL = "mongodb+srv://sam6238:<password>@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    ```

<br>

3. 設定 OpenAI API 密鑰並將其設置為環境變量。

    ```python
    import os
    from openai import OpenAI

    # 設置環境變數
    os.environ["OPENAI_API_KEY"] = toml.load("OPENAI_API_KEY")
    # 初始化 OpenAI 物件
    openai_client = OpenAI()
    ```

<br>

4. 下載評估數據集：使用 `Hugging Face` 的 `datasets` 庫來下載 `評估數據集`，並將其轉換為 `pandas dataframe`，數據集的關鍵列包括 `question`（用戶問題）、`correct_answer`（正確答案）和 `context`（參考文本）。

    ```python
    from datasets import load_dataset
    import pandas as pd

    data = load_dataset(
        "explodinggradients/ragas-wikiqa", split="train"
    )
    df = pd.DataFrame(data)
    ```

<br>

5. 創建參考文檔塊：將長的參考文本拆分成較小的塊以便於檢索，這是使用 `LangChain` 的 `RecursiveCharacterTextSplitter` 來完成的。

    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", keep_separator=False, chunk_size=200, chunk_overlap=30
    )

    def split_texts(texts):
        chunked_texts = []
        for text in texts:
            chunks = text_splitter.create_documents([text])
            chunked_texts.extend([chunk.page_content for chunk in chunks])
        return chunked_texts

    df["chunks"] = df["context"].apply(lambda x: split_texts(x))
    all_chunks = df["chunks"].tolist()
    docs = [item for chunk in all_chunks for item in chunk]
    ```

<br>

6. 創建嵌入並將其寫入 MongoDB：將文本塊轉換為嵌入並將其存儲到 MongoDB 中，這樣就可以用於檢索。

    ```python
    from pymongo import MongoClient
    from tqdm.auto import tqdm

    client = MongoClient(MONGODB_URI)
    DB_NAME = "ragas_evals"
    db = client[DB_NAME]
    batch_size = 128

    EVAL_EMBEDDING_MODELS = ["text-embedding-ada-002", "text-embedding-3-small"]

    def get_embeddings(docs, model):
        docs = [doc.replace("\n", " ") for doc in docs]
        response = openai_client.embeddings.create(input=docs, model=model)
        return [r.embedding for r in response.data]

    for model in EVAL_EMBEDDING_MODELS:
        embedded_docs = []
        print(f"Getting embeddings for the {model} model")
        for i in tqdm(range(0, len(docs), batch_size)):
            end = min(len(docs), i + batch_size)
            batch = docs[i:end]
            batch_embeddings = get_embeddings(batch, model)
            batch_embedded_docs = [
                {"text": batch[i], "embedding": batch_embeddings[i]}
                for i in range(len(batch))
            ]
            embedded_docs.extend(batch_embedded_docs)
        print(f"Finished getting embeddings for the {model} model")

        collection = db[model]
        collection.delete_many({})
        collection.insert_many(embedded_docs)
        print(f"Finished inserting embeddings for the {model} model")
    ```

<br>

_接下來，在 MongoDB Atlas UI 中為每個集合創建向量索引。_

7. 比較檢索嵌入模型：使用不同的嵌入模型來比較檢索效果，並評估檢索到的上下文的精度和召回率。

    ```python
    from langchain_openai import OpenAIEmbeddings
    from langchain_mongodb import MongoDBAtlasVectorSearch
    from langchain_core.vectorstores import VectorStoreRetriever

    def get_retriever(model, k):
        embeddings = OpenAIEmbeddings(model=model)
        vector_store = MongoDBAtlasVectorSearch.from_connection_string(
            connection_string=MONGODB_URI,
            namespace=f"{DB_NAME}.{model}",
            embedding=embeddings,
            index_name="vector_index",
            text_key="text",
        )
        return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})

    QUESTIONS = df["question"].to_list()
    GROUND_TRUTH = df["correct_answer"].tolist()

    from datasets import Dataset
    from ragas import evaluate, RunConfig
    from ragas.metrics import context_precision, context_recall
    import nest_asyncio

    nest_asyncio.apply()

    for model in EVAL_EMBEDDING_MODELS:
        data = {"question": [], "ground_truth": [], "contexts": []}
        data["question"] = QUESTIONS
        data["ground_truth"] = GROUND_TRUTH

        retriever = get_retriever(model, 2)
        for i in tqdm(range(0, len(QUESTIONS))):
            data["contexts"].append(
                [doc.page_content for doc in retriever.get_relevant_documents(QUESTIONS[i])]
            )
        dataset = Dataset.from_dict(data)
        run_config = RunConfig(max_workers=4, max_wait=180)
        result = evaluate(
            dataset=dataset,
            metrics=[context_precision, context_recall],
            run_config=run_config,
            raise_exceptions=False,
        )
        print(f"Result for the {model} model: {result}")
    ```

<br>

8. 比較生成模型：選擇最佳的檢索嵌入模型後，接著比較生成模型，並使用 RAG 鏈來生成答案。

    ```python
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.runnables.base import RunnableSequence
    from langchain_core.output_parsers import StrOutputParser

    def get_rag_chain(retriever, model):
        retrieve = {
            "context": retriever
            | (lambda docs: "\n\n".join([d.page_content for d in docs])),
            "question": RunnablePassthrough(),
        }
        template = """Answer the question based only on the following context: {context}\n\nQuestion: {question}"""
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatOpenAI(temperature=0, model=model)
        parse_output = StrOutputParser()
        return retrieve | prompt | llm | parse_output

    from ragas.metrics import faithfulness, answer_relevancy

    for model in ["gpt-3.5-turbo-1106", "gpt-3.5-turbo"]:
        data = {"question": [], "ground_truth": [], "contexts": [], "answer": []}
        data["question"] = QUESTIONS
        data["ground_truth"] = GROUND_TRUTH
        retriever = get_retriever("text-embedding-3-small", 2)
        rag_chain = get_rag_chain(retriever, model)
        for i in tqdm(range(0, len(QUESTIONS))):
            question = QUESTIONS[i]
            data["answer"].append(rag_chain.invoke(question))
            data["contexts"].append(
                [doc.page_content for doc in retriever.get_relevant_documents(question)]
            )
        dataset = Dataset.from_dict(data)
        run_config = RunConfig(max_workers=4, max_wait=180)
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy],
            run_config=run_config,
            raise_ex

    ceptions=False,
        )
        print(f"Result for the {model} model: {result}")
    ```

<br>

9. 測量 RAG 應用的整體性能：使用最佳的檢索和生成模型來評估整體系統的性能。

    ```python
    from ragas.metrics import answer_similarity, answer_correctness

    data = {"question": [], "ground_truth": [], "answer": []}
    data["question"] = QUESTIONS
    data["ground_truth"] = GROUND_TRUTH
    retriever = get_retriever("text-embedding-3-small", 2)
    rag_chain = get_rag_chain(retriever, "gpt-3.5-turbo")
    for question in tqdm(QUESTIONS):
        data["answer"].append(rag_chain.invoke(question))

    dataset = Dataset.from_dict(data)
    run_config = RunConfig(max_workers=4, max_wait=180)
    result = evaluate(
        dataset=dataset,
        metrics=[answer_similarity, answer_correctness],
        run_config=run_config,
        raise_exceptions=False,
    )
    print(f"Overall metrics: {result}")
    ```

<br>

10. 追蹤性能變化：在 MongoDB Atlas 中記錄評估結果，並使用 Atlas Charts 來追蹤和可視化性能，這樣可以在 MongoDB Atlas 中創建儀表板來可視化評估結果。。

    ```python
    from datetime import datetime

    result["timestamp"] = datetime.now()
    collection = db["metrics"]
    collection.insert_one(result)
    ```

<br>

___

_END_