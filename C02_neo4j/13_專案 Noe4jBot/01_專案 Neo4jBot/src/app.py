# app.py
import os

# 內建類型檢查模組
from typing import List, Union
import streamlit as st

# 繪圖工具庫
import graphviz

# 棄用或不適用
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
# 提供與 OpenAPI GPT 模型集成相關的功能
from langchain_openai import ChatOpenAI

# 用於處理圖形資料庫的互動
from langchain.graphs import Neo4jGraph

# 這兩個庫是用於定義人與 AI 間交換訊息的數據結構
from langchain.schema import HumanMessage, AIMessage

# 自訂函數
from cypher_chain import CYPHER_QA_PROMPT
from cypher_chain import CustomCypherChain

# 標題
st.title("VC Chatbot")

url = st.secrets["NEO4J_URI"]
username = st.secrets["NEO4J_USERNAME"]
password = st.secrets["NEO4J_PASSWORD"]
database = st.secrets["NEO4J_DATABASE"]

# Langchain x Neo4j connections
graph = Neo4jGraph(username=username, password=password, url=url, database=database)
#
graph_search = None

# Session state
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


# 自訂函數，生成回答文本，至少要傳入一個參數 `文本`
def generate_context(
    prompt: str, context_data: str = "generated"
) -> List[Union[AIMessage, HumanMessage]]:
    context = []
    # 假如存在查詢歷史紀錄
    if st.session_state["generated"]:
        # 加入最近的三筆查詢
        size = len(st.session_state["generated"])
        for i in range(max(size - 3, 0), size):
            context.append(HumanMessage(content=st.session_state["user_input"][i]))
            context.append(AIMessage(content=st.session_state[context_data][i]))
    # 加入本次的使用者查詢語句 `prompt`
    context.append(HumanMessage(content=str(prompt)))
    # 將處理後的文本列表傳出
    return context


# 用於建立並顯示 st 應用中的動態響應標籤，參數 `i` 當前處理對話的索引
def dynamic_response_tabs(i):
    # 初始化一個標籤列表，用於展示雙方對話
    tabs_to_add = ["💬Chat"]
    # 根據 `st.session_state` 檢查數據類型是否存在
    data_check = {
        "🔍Cypher": st.session_state["cypher"][i],
        "🗃️Database results": st.session_state["database"][i],
        "🕸️Visualization": st.session_state["viz_data"][i]
        # 進一步檢查 `viz_data` 是否有具體可用的可視化數據
        and st.session_state["viz_data"][i][0],
    }
    # 遍歷 `data_check`
    for tab_name, has_data in data_check.items():
        # 假如存在數據，則加入對話列表中 `tabs_to_add`
        if has_data:
            tabs_to_add.append(tab_name)
    # 使用 `with` 實現上下文管理器 `st.chat_message` 來顯示用戶輸入的訊息
    # 在這個區塊中，所有對話都會以氣泡顯示
    # `user` 代表的是顯示在用戶側
    with st.chat_message("user"):
        # 展示用戶的輸入
        st.write(st.session_state["user_input"][i])
    # 使用上下文管理器展示助手的回覆
    with st.chat_message("assistant"):
        # 建立一組標籤頁，每個標籤頁對應一個 `tabs_to_add`
        selected_tabs = st.tabs(tabs_to_add)
        # 根據不同的標籤頁來顯示不同的訊息
        with selected_tabs[0]:
            # 展示聊天內容
            st.write(st.session_state["generated"][i])
        if len(selected_tabs) > 1:
            with selected_tabs[1]:
                # 展示 Cypher 查詢程式碼
                st.code(st.session_state["cypher"][i], language="cypher")
        if len(selected_tabs) > 2:
            with selected_tabs[2]:
                # 顯示資料庫查詢結果
                st.write(st.session_state["database"][i])
        if len(selected_tabs) > 3:
            with selected_tabs[3]:
                # 建立一個圖，並添加節點和邊
                graph_object = graphviz.Digraph()
                for final_entity in st.session_state["viz_data"][i][1]:
                    graph_object.node(
                        final_entity, fillcolor="lightblue", style="filled"
                    )
                for record in st.session_state["viz_data"][i][0]:
                    graph_object.edge(
                        record["source"], record["target"], label=record["type"]
                    )
                st.graphviz_chart(graph_object)


# 自訂函數：取得使用者的輸入
def get_text() -> str:
    # 輸入框
    input_text = st.chat_input("誰是 Neo4j 的 CEO？")
    # 假如還沒輸出，檢查的邏輯是判斷有沒有以 `sk-` 開頭的字串
    if not openai_api_key.startswith("sk-"):
        # 標題之下會提示輸入
        st.warning("請輸入你的 OpenAI API key!", icon="⚠")
    else:
        return input_text


try:
    # 從 `sidebar` 框內取得
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    # 寫入環境參數，這在程序內運行，有生命週期，不會外洩
    os.environ["OPENAI_API_KEY"] = openai_api_key
    # 假如 True
    if openai_api_key:
        # 這是主要查詢的邏輯，使用圖形資料庫查詢鏈 `CustomCypherChain` 來建立實體
        graph_search = CustomCypherChain.from_llm(
            # 預設使用 `gpt-4-turbo`
            # temperature 範圍 0~1，越低代表越精準，這是自然語言領域中常見的一個參數
            # 用於生成 Cypher 查詢
            cypher_llm=ChatOpenAI(temperature=0.0, model_name="gpt-4-turbo"),
            # 用於處理與查詢相關的其他文本生成任務
            qa_llm=ChatOpenAI(temperature=0.0),
            # 用於執行生成的 Cypher 查詢
            graph=graph,
            # 用於生成查詢的提示模板，通過指定的格式引導 `qa_llm` 生成有用的回答
            qa_prompt=CYPHER_QA_PROMPT,
        )

    # 這是顯示在左側的文本
    st.sidebar.markdown(
        """
    ## Example questions

    * What do you know about Neo4j organization?
    * Who is Neo4j CEO?
    * How is Emil Eifrem connected to Magnus Christerson?
    * Which company has the most subsidiaries?
    * Who are the competitors of databricks?
    * How many levels of subsidiaries does Blackstone has?
    * Are there any news regarding employee satisfaction?
    * What are the latest news around companies where Emil Eifrem is CEO?
    * Are there any news about new partnerships mentioning Neo4j?

    You can also ask follow up questions as we use a conversational LLM under the hood.

    Code is available on [GitHub](https://github.com/tomasonjo/streamlit-neo4j-hackathon)
    """
    )

    # 調用自訂函數取得輸入框中使用者輸入的文本，這裡調用的函數僅做檢查，並未處理文本
    user_input = get_text()
    # 非零為 True
    if user_input:
        # 先顯示 `進行中`
        with st.spinner("Processing"):
            # 透過自訂函數處理使用者輸入的文本，主要是添加歷史查詢
            context = generate_context(user_input)
            # `graph_search` 是一個 `CustomCypherChain.from_llm` 物件
            # 傳入使用者輸入與歷史查詢
            print(f"=>輸出：user_input={user_input}", "\n")
            print(f"=>輸出：chat_history={context}", "\n")
            output = graph_search({"query": user_input, "chat_history": context})
            # session_state 是一個持久化儲存技術，將這些跨頁面的數據可以用字典的型態被儲存
            # 儲存當前對話
            st.session_state.user_input.append(user_input)
            # 儲存結果
            st.session_state.generated.append(output["result"])
            # 儲存可能生成的可視化數據
            st.session_state.viz_data.append(output["viz_data"])
            # 儲存與當前查詢相關的資料庫訊息
            st.session_state.database.append(output["database"])
            # 儲存生成的 Cypher 查詢（Query）
            st.session_state.cypher.append(output["cypher"])
    if st.session_state["generated"]:
        # 先計算鍵值 `generated` 的資料個數
        size = len(st.session_state["generated"])
        # 顯示最後三次互動
        for i in range(max(size - 3, 0), size):
            #
            dynamic_response_tabs(i)
except Exception as e:
    print(f"=>發生例外狀況：{e}")
finally:
    #
    print("=try 結束=")
