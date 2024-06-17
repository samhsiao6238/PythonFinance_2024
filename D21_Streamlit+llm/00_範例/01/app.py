import streamlit as st
# OpenAI 的 API
from openai import OpenAI

# 用於讀取敏感資訊
import os
from dotenv import load_dotenv
# 載入環境變數
load_dotenv()

# API密鑰和模型名稱
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")

# 使用側邊欄
with st.sidebar:
    "[查看源程式碼](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[其他參考資料 ...]()"

# 標題
st.title("💬 Chatbot")
# 說明文字
st.caption("🤖 這是使用 OpenAI 的 Streamlit 聊天機器人")

# 初始化聊天記錄，如果 session_state 中沒有 messages，則設置初始消息
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        # 設置初始的助手消息：這是機器人預設講的第一句話
        {"role": "assistant", "content": "你需要什麼幫助嗎？"}
    ]

# 遍歷 messages 列表中的消息
for msg in st.session_state.messages:
    # 顯示每條消息的內容
    st.chat_message(msg["role"]).write(msg["content"])

# 當用戶輸入新的消息時，將其添加到聊天記錄中並顯示
# 這裡使用型別判斷
if prompt := st.chat_input():
    # 如果沒有提供API密鑰，顯示提示信息並停止應用
    if not OPENAI_API_KEY:
        # 顯示提示信息
        st.info("請更新 OpenAI API key 的資訊再繼續。")
        # 停止應用
        st.stop()

    # 使用提供的API密鑰建立OpenAI客戶端
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    # 將用戶 `user` 的消息添加到聊天記錄中
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 顯示用戶發送的消息
    st.chat_message("user").write(prompt)

    # 回應之前要處理的工作寫在這裡...

    # 向 OpenAI API 發送請求，取得助手回應
    # 可添加 `temperature` 參數
    response = client.chat.completions.create(
        # 指定使用的模型
        model=OPENAI_API_MODEL,
        # 傳遞所有聊天記錄作為上下文
        messages=st.session_state.messages,
        # 設置 temperature 參數，若未設定預設值為 1.0，表示 `較高的隨機與創意`
        # `temperature` 範圍通常為 0.0 到 2.0 之間，超過 1.0 之後就相對隨機
        temperature=1.0
    )
    # 取得API返回的回應內容
    msg = response.choices[0].message.content
    # 將助手回應添加到聊天記錄中
    st.session_state.messages.append({"role": "assistant", "content": msg})
    # 顯示助手的回應
    st.chat_message("assistant").write(msg)
