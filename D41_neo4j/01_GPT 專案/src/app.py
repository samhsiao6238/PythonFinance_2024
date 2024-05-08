"""
這是一個完整的Streamlit和Langchain的集成腳本，旨在利用OpenAI的語言模型和Neo4j圖形資料庫進行對話。
"""

import os

# 載入 dotenv
from dotenv import load_dotenv

#
from typing import List, Union
import streamlit as st

# 用於創建和呈現圖形結構
import graphviz

# 從Langchain引入用於OpenAI聊天模型的封裝
from langchain.chat_models import ChatOpenAI

# 引入Langchain對Neo4j圖形資料庫的封裝
from langchain.graphs import Neo4jGraph

# 引入Langchain消息架構
from langchain.schema import HumanMessage, AIMessage

# 引入自定義的Cypher鏈和提問提示
from cypher_chain import CYPHER_QA_PROMPT, CustomCypherChain

# 載入環境變數
load_dotenv()

# 設置OpenAI API Key
openai_api_key = os.getenv("OPENAPI_API_KEY")
# 將API鍵設定為環境變數
os.environ["OPENAI_API_KEY"] = openai_api_key

# 設定Streamlit頁面標題
st.title("VC Chatbot")

# 設定Neo4j資料庫的連接信息
url = "neo4j+s://demo.neo4jlabs.com"
username = "companies"
password = "companies"
database = "companies"

# 創建一個Neo4j圖形資料庫實例
graph = Neo4jGraph(username=username, password=password, url=url, database=database)

# 從語言模型創建自定義的Cypher查詢鏈
graph_search = CustomCypherChain.from_llm(
    # 設置OpenAI聊天模型
    cypher_llm=ChatOpenAI(temperature=0.0, model_name="gpt-4"),
    # 設置用於問答的OpenAI模型
    qa_llm=ChatOpenAI(temperature=0.0),
    # 指定圖形資料庫，傳入前一個步驟建立的資料庫實例
    graph=graph,
    # 設置查詢提示，這是從自訂模組中導入的
    qa_prompt=CYPHER_QA_PROMPT,
)

# 初始化 session state，確保每次執行應用程式時，相關的數據和變量都被正確設置和跟踪
# 在 Streamlit 應用中，`st.session_state`` 是用在跨頁面請求時保存狀態的工具
# 檢查是否包含了特定的 key，如果沒有就初始化並賦予一個空列表
# 可確保這些鍵在後續操作中已經被定義並可用於儲存數據。
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "user_input" not in st.session_state:
    st.session_state["user_input"] = []

if "viz_data" not in st.session_state:
    st.session_state["viz_data"] = []

if "database" not in st.session_state:
    st.session_state["database"] = []

if "cypher" not in st.session_state:
    st.session_state["cypher"] = []

# 生成聊天機器下回應的上下文
"""參數與回傳值：
prompt: 字串，表示當前用戶的輸入。
context_data: 字串，預設為 "generated"，用來指定從 st.session_state 中讀取哪個對話數據，通常是用來指定是從哪類型的消息中抽取歷史數據。
返回一個列表，包含混合類型的 AIMessage 和 HumanMessage 對象，這些對象代表了生成回應所需的上下文。
"""


def generate_context(
    prompt: str, context_data: str = "generated"
) -> List[Union[AIMessage, HumanMessage]]:
    # 建立空列表用來儲存對話的上下文
    context = []
    # 假如有歷史對話
    if st.session_state["generated"]:
        # 先計算歷史對話的數量
        size = len(st.session_state["generated"])
        # 只取最後三條對話進行上下文生成
        for i in range(max(size - 3, 0), size):
            # 把每條對話中 `用戶的輸入`與`AI的回應`添加到 `context` 列表
            context.append(HumanMessage(content=st.session_state["user_input"][i]))
            context.append(AIMessage(content=st.session_state[context_data][i]))
    # 先將當前用戶的輸入 `prompt` 轉換為 `HumanMessage` 物件，
    # 再將用戶的輸入，然後添加到 `context`
    context.append(HumanMessage(content=str(prompt)))
    # 傳出
    return context


# 動態生成多個響應標籤（Tabs），並根據用戶與 AI 對話的內容和結果來展示相應的數據和視覺化信息
"""參數
i：表示要展示的對話和相關數據在列表中的索引
"""


def dynamic_response_tabs(i):
    # 建立一個列表 tabs_to_add，預設包含 `💬Chat` 標籤，此標籤用於展示用戶和 AI 的對話
    tabs_to_add = ["💬Chat"]
    # 定義一個字典來儲存各類數據的存在檢查
    data_check = {
        # 展示生成的 Cypher 查詢語句
        "🔍Cypher": st.session_state["cypher"][i],
        # 展示從資料庫查詢的結果
        "🗃️Database results": st.session_state["database"][i],
        # 展示數據的視覺化，此處使用了 `短路評估` 確保對應數據索引存在
        "🕸️Visualization": st.session_state["viz_data"][i]
        and st.session_state["viz_data"][i][0],
    }

    # 遍歷 data_check，將有數據的標籤加入到前面建立的列表 `tabs_to_add`
    for tab_name, has_data in data_check.items():
        if has_data:
            tabs_to_add.append(tab_name)

    # 創建一個對話框來展示用戶的輸入
    with st.chat_message("user"):
        # 展示指定索引的用戶輸入
        st.write(st.session_state["user_input"][i])
    # 創建一個對話框來展示助理的回應
    with st.chat_message("assistant"):
        # 創建多個標籤，根據先前檢查的數據類型動態添加
        selected_tabs = st.tabs(tabs_to_add)
        # 遍歷並展示每個標籤對應的內容
        with selected_tabs[0]:
            st.write(st.session_state["generated"][i])
        # 假如數量多於 1
        if len(selected_tabs) > 1:
            # 第一個標籤始終展示 AI 生成的回應
            with selected_tabs[1]:
                st.code(st.session_state["cypher"][i], language="cypher")
        # 如果有額外的標籤，則根據其類型展示 Cypher 語句、資料庫結果或視覺化內容
        if len(selected_tabs) > 2:
            with selected_tabs[2]:
                st.write(st.session_state["database"][i])
        if len(selected_tabs) > 3:
            with selected_tabs[3]:
                # 若存在視覺化數據，則使用 graphviz.Digraph() 創建一個有向圖
                graph_object = graphviz.Digraph()
                # 添加節點和邊
                # 根據 st.session_state["viz_data"][i] 儲存的視覺化數據建立圖形
                for final_entity in st.session_state["viz_data"][i][1]:
                    graph_object.node(
                        final_entity, fillcolor="lightblue", style="filled"
                    )
                for record in st.session_state["viz_data"][i][0]:
                    graph_object.edge(
                        record["source"], record["target"], label=record["type"]
                    )
                # 在 Streamlit 應用中渲染視覺化圖形
                st.graphviz_chart(graph_object)


# 提供用戶輸入界面
user_input = st.chat_input("Who is the CEO of Neo4j?")

if user_input:
    # 顯示加載動畫
    with st.spinner("Processing"):
        # 生成對話上下文
        context = generate_context(user_input)
        # 執行圖形搜索和語言模型處理
        output = graph_search({"query": user_input, "chat_history": context})

        # 儲存結果到session state
        st.session_state.user_input.append(user_input)
        st.session_state.generated.append(output["result"])
        st.session_state.viz_data.append(output["viz_data"])
        st.session_state.database.append(output["database"])
        st.session_state.cypher.append(output["cypher"])

# 展示生成的對話
if st.session_state["generated"]:
    size = len(st.session_state["generated"])
    for i in range(max(size - 3, 0), size):
        dynamic_response_tabs(i)
