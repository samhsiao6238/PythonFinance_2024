# Bot

_範例的 [教程網址](https://graphacademy.neo4j.com/courses/llm-chatbot-python/1-project-setup/)_

![](images/img_01.png)

可參考 [GitHub](https://github.com/neo4j-graphacademy/llm-chatbot-python?tab=readme-ov-file)

_待續_

## 步驟

因為 `Langchain` 模組不支援 `Python 3.12` 以上版本，所以要查詢並確認當前環境的版本號可用。
```bash
python --version
```

建立虛擬環境。
```bash
python -m venv envllmChatBot
```

修改環境參數
```bash
sudo nano ~/.zshrc
```

加入，然後儲存 `control+o`、退出 `control+x`
```bash
source /Users/samhsiao/Documents/PythonVenv/envllmChatBot/bin/activate
```

啟動虛擬環境
```bash
source ~/.zshrc
```

進入要存放的路徑中，這裡示範存放在桌面，然後下載 git，並進入下載的資料夾。
```bash
cd ~/Desktop && git clone https://github.com/neo4j-graphacademy/llm-chatbot-python && cd llm-chatbot-python
```

透過指令安裝套件
```bash
pip install -r requirements.txt
```

另外安裝一個套件，因為沒安裝在後面會出現錯誤
```bash
pip install langchainhub
```

如指示更新就照做
```bash
pip install --upgrade pip
```

嘗試運行主腳本 `bot.py`。
```bash
streamlit run bot.py
```

當前的機器人只會回應相同訊息
![](images/img_02.png)

退出運行 `control+c` 並開啟 VSCode
```bash
code .
```

## 建立 LLM 實體

進入 [OpenAI 官網]( platform.openai.com) 取得 API Key，這裡先跳過。

在本地運行，所以使用 `.env`，儲存 `OPENAI_API_KEY` 及 `OPENAI_MODEL`，先運行 `gpt-3.5-turbo` 試試，或是換作 `GPT-4` 試試。
```bash
touch .env .gitignore
```

編輯 `.gitignore`
```json
.env
```

在 `.env` 寫入敏感資訊，其中 `OPENAI_MODEL` 查詢官網
```json
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
```

安裝套件
```bash
pip install python-dotenv
```


改寫官方的 `llm.py`
```python
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
# 環境變數
import os
from dotenv import load_dotenv
#
load_dotenv()

# 取得環境變數
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# 建立 ChatOpenAI 實體
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
)

# OpenAIEmbeddings 是用來生成和處理嵌入向量（embeddings）
# 這些嵌入向量是從使用 OpenAI 模型（如 GPT-4）生成的文本中獲取的
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

```

建立 Sandbox
![](images/img_03.png)

展開可查看訊息，這與教程寫的一樣。
```bash
# Connection URL
3.239.239.7
# Username
neo4j
# Password
hitch-humans-menu
```
![](images/img_04.png)

修改 `.env` 文件，將 Sandbox 資訊寫入。
```bash
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo

NEO4J_URI = "bolt://3.239.239.7:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "hitch-humans-menu"
```

接著編輯 `graph.py`。
```bash
from langchain_community.graphs import Neo4jGraph
# dotenv
import os
from dotenv import load_dotenv
# 環境參數
load_dotenv()

# 取得環境變數
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Neo4j Graph
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

```

接著編輯 `agent.py`
```python
# agent.py
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from solutions.llm import llm
from solutions.tools.vector import kg_qa
from solutions.tools.finetuned import cypher_qa

# tools 的列表定義了其他狀況發生時的設定
tools = [
    Tool.from_function(
        name="General Chat",
        description="For general chat not covered by other tools",
        func=llm.invoke,
        return_direct=True,
    ),
    Tool.from_function(
        name="Cypher QA",
        description="Provide info about movies questions using Cypher",
        func=cypher_qa,
        return_direct=True,
    ),
    Tool.from_function(
        name="Vector Search Index",
        description="Provides info about movie plots using Vector Search",
        func=kg_qa,
        return_direct=True,
    ),
]

# 調用 langchain 函數 ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True,
)

# 調用 langchain 函數 hub.pull() 生成
agent_prompt = hub.pull("hwchase17/react-chat")
# 調用 langchain 函數 create_react_agent，傳入 `llm`、`tools`、`Agent 的回應`
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, memory=memory, verbose=True
)

# 這是原本的函數，改寫添加了判斷的機制
# def generate_response(prompt):
#     response = agent_executor.invoke({"input": prompt})
#     return response["output"]


def generate_response(prompt):
    try:
        # 回應
        response = agent_executor.invoke({"input": prompt})
        #
        if isinstance(response['output'], dict):
            print('=agent.py -> 備註：回應是一個 dict=')
            response_output = ''
            for item in response['output']:
                if response_output:
                    response_output += ', '
                response_output += str(item)
        else:
            # 回應訊息
            print('=agent.py -> 備註：回應訊息=')
            response_output = str(response['output'])
        return response_output
    except Exception as e:
        print('=agent.py -> 備註：回應發生錯誤=')
        return f"Error processing response: {str(e)}"

```

改寫 `graph.py`
```python
from langchain_community.graphs import Neo4jGraph
# dotenv
import os
from dotenv import load_dotenv
# 環境參數
load_dotenv()

# 取得環境變數
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Neo4j Graph
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

```

改寫 `vector.py`。
```python
# vector.py
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import RetrievalQA
from solutions.llm import llm, embeddings
#
import os
from dotenv import load_dotenv
#
load_dotenv()

#
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                 # <1>
    url=NEO4J_URI,              # <2>
    username=NEO4J_USERNAME,    # <3>
    password=NEO4J_PASSWORD,    # <4>
    index_name="moviePlots",    # <5>
    node_label="Movie",         # <6>
    text_node_property="plot",  # <7>
    embedding_node_property="plotEmbedding",  # <8>
    retrieval_query="""
    RETURN
        node.plot AS text,
        score,
        {
            title: node.title,
            directors: [ (person)-[:DIRECTED]->(node) | person.name ],
            actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
            tmdbId: node.tmdbId,
            source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
        } AS metadata
    """,
)

retriever = neo4jvector.as_retriever()

kg_qa = RetrievalQA.from_chain_type(
    llm,  # <1>
    chain_type="stuff",  # <2>
    retriever=retriever,  # <3>
)

```