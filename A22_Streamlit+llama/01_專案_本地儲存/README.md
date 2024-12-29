# 範例專案

[參考網址](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/docs/examples/agent/Chatbot_SEC.ipynb#scrollTo=35c20fbe)

以下是根據您提供的教程製作的一個完整教學指引和範例腳本。這個教學將帶您一步步完成一個基於LLM（大型語言模型）的上下文增強聊天機器人。該聊天機器人可以智能地執行各種數據查詢任務，如問題回答和摘要生成。

## 完整範例腳本

### 第一步：準備環境

在開始之前，請確保安裝必要的Python包。請運行以下命令來安裝這些包：

```bash
pip install llama-index-readers-file
pip install llama-index-embeddings-openai
pip install llama-index-agent-openai
pip install llama-index-llms-openai
pip install nest_asyncio
```

### 第二步：設置環境變數和啟動環境

將自己的OpenAI API密鑰設置為環境變數，並確保在Jupyter Notebook中正確顯示輸出。

```python
import os
import nest_asyncio
from IPython.display import HTML, display

os.environ["OPENAI_API_KEY"] = "sk-..."  # 更改為自己的OpenAI API密鑰

nest_asyncio.apply()

def set_css():
    display(HTML("""
    <style>
        pre {
            white-space: pre-wrap;
        }
    </style>
    """))

get_ipython().events.register("pre_run_cell", set_css)
```

### 第三步：下載和解析數據

下載UBER的10-K文件並使用Unstructured庫解析HTML文件。

```python
# 下載UBER 10-K文件
!mkdir data
!wget "https://www.dropbox.com/s/948jr9cfs7fgj99/UBER.zip?dl=1" -O data/UBER.zip
!unzip data/UBER.zip -d data

from llama_index.readers.file import UnstructuredReader
from pathlib import Path

years = [2022, 2021, 2020, 2019]

loader = UnstructuredReader()
doc_set = {}
all_docs = []
for year in years:
    year_docs = loader.load_data(file=Path(f"./data/UBER/UBER_{year}.html"), split_documents=False)
    for d in year_docs:
        d.metadata = {"year": year}
    doc_set[year] = year_docs
    all_docs.extend(year_docs)
```

### 第四步：設置向量索引

為每個年份建立向量索引並保存到磁碟。

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

index_set = {}
for year in years:
    storage_context = StorageContext.from_defaults()
    cur_index = VectorStoreIndex.from_documents(doc_set[year], storage_context=storage_context)
    index_set[year] = cur_index
    storage_context.persist(persist_dir=f"./storage/{year}")
```

### 第五步：從磁碟載入索引

從磁碟載入索引。

```python
from llama_index.core import load_index_from_storage

index_set = {}
for year in years:
    storage_context = StorageContext.from_defaults(persist_dir=f"./storage/{year}")
    cur_index = load_index_from_storage(storage_context)
    index_set[year] = cur_index
```

### 第六步：設置子問題查詢引擎

建立子問題查詢引擎來綜合跨年度的10-K文件答案。

```python
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine

individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=index_set[year].as_query_engine(),
        metadata=ToolMetadata(
            name=f"vector_index_{year}",
            description=(f"useful for when you want to answer queries about the {year} SEC 10-K for Uber")
        )
    ) for year in years
]

query_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=individual_query_engine_tools)
```

### 第七步：設置聊天機器人代理

設置外部聊天機器人代理，使用先前定義的工具來處理查詢。

```python
from llama_index.agent.openai import OpenAIAgent

query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="sub_question_query_engine",
        description=("useful for when you want to answer queries that require analyzing multiple SEC 10-K documents for Uber")
    )
)

tools = individual_query_engine_tools + [query_engine_tool]

agent = OpenAIAgent.from_tools(tools, verbose=True)
```

### 第八步：測試代理

測試代理處理不同的查詢。

```python
response = agent.chat("hi, i am bob")
print(str(response))

response = agent.chat("What were some of the biggest risk factors in 2020 for Uber?")
print(str(response))

cross_query_str = (
    "Compare/contrast the risk factors described in the Uber 10-K across years. Give answer in bullet points."
)
response = agent.chat(cross_query_str)
print(str(response))
```

### 第九步：設置互動循環

設置一個簡單的互動循環來與SEC增強的聊天機器人互動。

```python
agent = OpenAIAgent.from_tools(tools)  # verbose=False by default

while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    response = agent.chat(text_input)
    print(f"Agent: {response}")

# User: What were some of the legal proceedings against Uber in 2022?
# Agent: (回應例子)
```

### 完整腳本

```python
# 完整腳本
import os
import nest_asyncio
from IPython.display import HTML, display
from llama_index.readers.file import UnstructuredReader
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.agent.openai import OpenAIAgent

# 設置環境變數
os.environ["OPENAI_API_KEY"] = "sk-..."  # 更改為自己的OpenAI API密鑰
nest_asyncio.apply()

def set_css():
    display(HTML("""
    <style>
        pre {
            white-space: pre-wrap;
        }
    </style>
    """))

get_ipython().events.register("pre_run_cell", set_css)

# 下載並解析數據
!mkdir data
!wget "https://www.dropbox.com/s/948jr9cfs7fgj99/UBER.zip?dl=1" -O data/UBER.zip
!unzip data/UBER.zip -d data

years = [2022, 2021, 2020, 2019]

loader = UnstructuredReader()
doc_set = {}
all_docs = []
for year in years:
    year_docs = loader.load_data(file=Path(f"./data/UBER/UBER_{year}.html"), split_documents=False)
    for d in year_docs:
        d.metadata = {"year": year}
    doc_set[year] = year_docs
    all_docs.extend(year_docs)

# 設置向量索引
Settings.chunk_size = 512
Settings.chunk_overlap = 64
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

index_set = {}
for year in years:
    storage_context = StorageContext.from_defaults()
    cur_index = VectorStoreIndex.from_documents(doc_set[year], storage_context=storage_context)
    index_set[year] = cur_index
    storage_context.persist(persist_dir=f"./storage/{year}")

# 從磁碟載入索引
index_set = {}
for year in years:
    storage_context = StorageContext.from_defaults(persist_dir=f"./storage/{year}")
    cur_index = load_index_from_storage(storage_context)
    index_set[year] = cur_index

# 設置子問題查詢引擎
individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=index_set[year].as_query_engine(),
        metadata=ToolMetadata(
            name=f"vector_index_{year}",
            description=(f"useful for when you want to answer queries about the {year} SEC 10-K for Uber")
        )
    ) for year in years
]

query_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=individual_query_engine_tools)

# 設置聊天機器人代理
query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="sub_question_query_engine",
        description=("useful for when you want to answer queries that require analyzing multiple SEC 10-K documents for Uber")
    )
)

tools

 = individual_query_engine_tools + [query_engine_tool]
agent = OpenAIAgent.from_tools(tools, verbose=True)

# 測試代理
response = agent.chat("hi, i am bob")
print(str(response))

response = agent.chat("What were some of the biggest risk factors in 2020 for Uber?")
print(str(response))

cross_query_str = (
    "Compare/contrast the risk factors described in the Uber 10-K across years. Give answer in bullet points."
)
response = agent.chat(cross_query_str)
print(str(response))

# 設置互動循環
agent = OpenAIAgent.from_tools(tools)

while True:
    text_input = input("User: ")
    if text_input == "exit":
        break
    response = agent.chat(text_input)
    print(f"Agent: {response}")
```

這個完整的範例腳本將指引您一步步地建立一個上下文增強的聊天機器人，並能夠智能地回答有關UBER 10-K文件的問題。通過這個過程，您可以了解如何利用LlamaIndex和OpenAI的API來處理和查詢大量文本數據。