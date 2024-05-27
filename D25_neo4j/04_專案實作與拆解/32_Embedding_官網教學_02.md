# 官網教學

[Part 1](https://www.mongodb.com/developer/products/atlas/choose-embedding-model-rag/)

[Part 2](https://www.mongodb.com/developer/products/atlas/evaluate-llm-applications-rag/)


## 說明

1. 安裝所需的庫

這一步涉及安裝本文中所需的所有 Python 庫。以下是相關的代碼：

```python
!pip install -qU datasets ragas langchain langchain-mongodb langchain-openai pymongo pandas tqdm matplotlib seaborn
```

這些庫包括：
- `datasets`：從 Hugging Face Hub 獲取數據集。
- `ragas`：RAGAS 框架，用於評估 RAG 應用。
- `langchain`：用於開發 LLM 應用。
- `langchain-mongodb`：用於將 MongoDB Atlas 作為向量存儲使用。
- `langchain-openai`：用於在 LangChain 中使用 OpenAI 模型。
- `pymongo`：用於與 MongoDB 交互的 Python 驅動。
- `pandas`：用於數據分析、探索和操作。
- `tdqm`：顯示進度條。
- `matplotlib` 和 `seaborn`：用於數據可視化。

### Step 2: 設置先決條件

在這一步，我們設置了 MongoDB Atlas 作為向量存儲並獲取連接字符串。

#### 步驟：
1. 註冊 MongoDB Atlas 帳戶。
2. 創建數據庫集群。
3. 獲取連接字符串。
4. 將主機機器的 IP 添加到集群的 IP 訪問列表中。

#### 代碼：
```python
import getpass
MONGODB_URI = getpass.getpass("Enter your MongoDB connection string:")
```

我們還需要獲取 OpenAI API 密鑰並將其設置為環境變量：

```python
import os
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API Key:")
openai_client = OpenAI()
```

### Step 3: 下載評估數據集

我們使用 Hugging Face 的 `datasets` 庫來下載評估數據集，並將其轉換為 pandas dataframe。

#### 代碼：
```python
from datasets import load_dataset
import pandas as pd

data = load_dataset("explodinggradients/ragas-wikiqa", split="train")
df = pd.DataFrame(data)
```

數據集的關鍵列包括 `question`（用戶問題）、`correct_answer`（正確答案）和 `context`（參考文本）。

### Step 4: 創建參考文檔塊

我們將長的參考文本拆分成較小的塊，以便於檢索。這是使用 LangChain 的 `RecursiveCharacterTextSplitter` 來完成的。

#### 代碼：
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

### Step 5: 創建嵌入並將其寫入 MongoDB

我們將文本塊轉換為嵌入並將其存儲到 MongoDB 中，這樣就可以用於檢索。

#### 代碼：
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

接下來，在 MongoDB Atlas UI 中為每個集合創建向量索引。

### Step 6: 比較檢索嵌入模型

我們使用不同的嵌入模型來比較檢索效果，並評估檢索到的上下文的精度和召回率。

#### 代碼：
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

### Step 7: 比較生成模型

我們選擇最佳的檢索嵌入模型後，接著比較生成模型，並使用 RAG 鏈來生成答案。

#### 代碼：
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

### Step 8: 測量 RAG 應用的整體性能

使用最佳的檢索和生成模型來評估整體系統的性能。

#### 代碼：
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

### Step 9: 追蹤性能變化

最後，我們在 MongoDB Atlas 中記錄評估結果，並使用 Atlas Charts 來追蹤和可視化性能。

#### 代碼：
```python
from datetime import datetime

result["timestamp"] = datetime.now()
collection = db["metrics"]
collection.insert_one(result)
```

這樣，我們可以在 MongoDB Atlas 中創建儀表板來可視化評估結果。

### 結論

這個教程分別展示了如何安裝必要的工具、設置數據庫和 API 密鑰、下載和處理數據集、生成嵌入並存儲到 MongoDB 中，然後使用這些嵌入來進行檢索和生成，最後評估整體系統的性能並追蹤變化。這些步驟確保了我們能夠高效地評估和改進我們的 LLM 應用。