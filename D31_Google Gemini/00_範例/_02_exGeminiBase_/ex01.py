import os
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# 加載 .env 文件
load_dotenv()

# 確保 GEMINI_API_KEY 已經設置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY is None:
    st.error("環境變量 GEMINI_API_KEY 未設置，請檢查 .env 文件。")
    st.stop()

# Streamlit 應用程序標題
st.title("Gemini API Text Generator")

# 配置流式輸出參數
# 限制隊列中可保留的輸出數量
st.session_state.max_queued_outputs = 10
# 輸出生成之間的間隔時間，以秒為單位
st.session_state.report_interval = 0.5
# 是否僅在有請求時才生成輸出
st.session_state.on_demand = False

# 獲取用戶輸入
user_input = st.text_input("在此輸入問題：")

if st.button("產生"):
    try:
        if not user_input:
            st.warning("請輸入一些說明。")
        else:
            # 假設模型名稱是 gemini-pro
            model_name = "gemini-pro"
            model = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=GEMINI_API_KEY
            )
            message = HumanMessage(content=user_input)
            response = model.stream([message])

            # 創建一個空的 Streamlit 元素以便流式更新
            output_placeholder = st.empty()
            generated_text = ""

            # 使用流式方式逐步顯示生成的文本
            for chunk in response:
                generated_text += chunk.content
                # 實時更新生成的文本
                output_placeholder.text(generated_text)

            st.success("生成文字已完成。")

    except Exception as e:
        st.error(f"發生錯誤： {str(e)}")
