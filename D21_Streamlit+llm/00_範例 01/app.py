import streamlit as st
# OpenAI 的 API
from openai import OpenAI

# 用於讀取敏感資訊
import os
from dotenv import load_dotenv
# 加載環境變數
load_dotenv()

# API密鑰和模型名稱
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")

# 使用側邊欄
with st.sidebar:
    "[取得 OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[查看代碼](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

# 標題
st.title("💬 Chatbot")
# 說明文字
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# 初始化聊天記錄，如果session_state中沒有messages，則設置初始消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        # 設置初始的助手消息
        {"role": "assistant", "content": "How can I help you?"}
    ]

# 迭代顯示messages列表中的消息
for msg in st.session_state.messages:
    # 顯示每條消息的內容
    st.chat_message(msg["role"]).write(msg["content"])

# 當用戶輸入新的消息時，將其添加到聊天記錄中並顯示
if prompt := st.chat_input():
    # 如果沒有提供API密鑰，顯示提示信息並停止應用
    if not OPENAI_API_KEY:
        # 顯示提示信息
        st.info("請更新 OpenAI API key 的資訊再繼續。")
        # 停止應用
        st.stop()

    # 使用提供的API密鑰創建OpenAI客戶端
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    # 將用戶消息添加到聊天記錄中
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 顯示用戶的消息
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        # 指定使用的模型
        model=OPENAI_API_MODEL,
        # 傳遞所有聊天記錄作為上下文
        messages=st.session_state.messages
    )
    # 獲取API返回的回應內容
    msg = response.choices[0].message.content
    # 將助手回應添加到聊天記錄中
    st.session_state.messages.append({"role": "assistant", "content": msg})
    # 顯示助手的回應
    st.chat_message("assistant").write(msg)
