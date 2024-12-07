# 範例一：這是一個 Streamlit 的範例
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


# Google Gemini API 金鑰
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
# 檢查是否存在
if GEMINI_API_KEY is None:
    st.error("環境變數 GEMINI_API_KEY 未設置，請檢查 .env 文件。")
    st.stop()

# 使用模型
model_name = "gemini-pro"
# 建立模型
model = ChatGoogleGenerativeAI(
    model=model_name,
    google_api_key=GEMINI_API_KEY
)

# 設置 Streamlit 標題
st.title("Gemini API 文本生成器")

# 建立文本輸入框讓用戶輸入問題
user_input = st.text_input("請輸入你的問題：")

# 當用戶點擊 `生成` 按鈕時執行的操作
if st.button("生成"):
    if not user_input:
        st.warning("請輸入一些文本。")
    else:
        try:
            # 依據用戶輸入，建立 HumanMessage 實體
            message = HumanMessage(content=user_input)
            # 傳入 `HumanMessage 實體`，並使用模型生成回應文本
            response = model.stream([message])
            # 建立一個空的 Streamlit 元件，以便後續更新輸出
            output_placeholder = st.empty()
            generated_text = ""

            # 使用流式方式逐步顯示生成的文本
            for chunk in response:
                generated_text += chunk.content
                output_placeholder.text(generated_text)

            # 顯示成功訊息，指示文本生成完成
            st.success("文本生成已完成。")

        except Exception as e:
            st.error(f"發生錯誤： {str(e)}")
