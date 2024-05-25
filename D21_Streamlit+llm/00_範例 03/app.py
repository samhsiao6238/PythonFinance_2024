import streamlit as st
# 用於初始化代理
from langchain.agents import initialize_agent, AgentType
# 用於處理回調
from langchain.callbacks import StreamlitCallbackHandler
# 用於使用OpenAI的聊天模型
from langchain.chat_models import ChatOpenAI
# 用於進行DuckDuckGo的搜索
from langchain.tools import DuckDuckGoSearchRun

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_API_MODEL = st.secrets["OPENAI_API_MODEL"]

# 側邊欄
with st.sidebar:
    "[取得 OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[原始碼](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"

# 設置應用的標題
st.title("🔎 LangChain - Chat with search")

# 設置應用的描述
"""
在此範例中，使用 StreamlitCallbackHandler，在互動式 Streamlit 應用程式中顯示代理程式的想法和操作。
嘗試更多 LangChain 🤝 Streamlit Agent 範例，可參考 [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent)。
"""

# 如果session_state中沒有messages，初始化一個包含歡迎消息的messages列表
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "哈囉，我是一個可協助進行網路搜尋的機器人，你想搜尋什麼？"}
    ]

# 迭代顯示messages列表中的消息
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 如果用戶輸入了新的問題，將其添加到messages列表中並顯示
if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 如果沒有提供OpenAI API密鑰，顯示提示信息並停止應用
    if not OPENAI_API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # 使用提供的API密鑰和模型名稱初始化ChatOpenAI對象
    llm = ChatOpenAI(
        model_name=OPENAI_API_MODEL,
        openai_api_key=OPENAI_API_KEY,
        streaming=True
    )
    # 初始化DuckDuckGo搜索工具
    search = DuckDuckGoSearchRun(name="Search")
    # 初始化搜索代理，並設置代理類型和錯誤處理
    search_agent = initialize_agent(
        [search],
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )
    # 建立一個新的聊天消息塊，顯示助手的回應
    with st.chat_message("assistant"):
        # 初始化回調處理器
        st_cb = StreamlitCallbackHandler(
            st.container(),
            expand_new_thoughts=False
        )
        # 執行搜索代理並獲取回應
        response = search_agent.run(
            st.session_state.messages,
            callbacks=[st_cb]
        )
        # 將回應添加到messages列表中
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        # 顯示回應
        st.write(response)
