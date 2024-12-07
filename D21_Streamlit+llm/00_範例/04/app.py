'''
LangChain使用的OpenAI API對生成的文本長度有預設的限制。
如果你想增加生成回應的長度，可以設置max_tokens參數來指定生成的最大token數量。
'''
import streamlit as st
from langchain.llms import OpenAI

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_API_MODEL = st.secrets["OPENAI_API_MODEL"]

# 標題
st.title("🦜🔗 Langchain Quickstart App")

with st.sidebar:
    _temp = st.text_input("請輸入敏感資訊", type="password")
    "[取得 OpenAI API key](https://platform.openai.com/account/api-keys)"


# 自訂函數：生成回應訊息
def generate_response(input_text):
    # 建立語言模型對象，可用於生成自然語言文本，`溫度` 越高則變化性越大
    # 根據提示 `prompt` 生成連續的文本
    llm = OpenAI(
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY,
        max_tokens=400
    )
    # 透過 `llm` 對輸入文字 `input_text` 作出回覆文本，並使用 `info` 輸出回應
    st.info(llm(input_text))


# `st.form` 建立表單的函數，`my_form` 是表單的識別名稱，可用於管理、處理表單的提交事件
with st.form("my_form"):
    # 輸入要查詢的文字
    text = st.text_area("輸入文字：", "學習程式設計的 3 個關鍵建議是什麼？")
    # 按鈕：傳送
    submitted = st.form_submit_button("Submit")
    # 假如沒有 Key
    if not OPENAI_API_KEY:
        st.info("請新增自己的 OpenAI API 金鑰以繼續。")
    elif submitted:
        # 調用自訂函數
        generate_response(text)
