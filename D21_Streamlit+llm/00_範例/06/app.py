# 使用 openai 的 OpenAI
from openai import OpenAI
import streamlit as st
# streamlit_feedback 用於收集用戶反饋
# 每次回應後會顯示一個反饋界面，讓用戶對語言模型的回應進行評價
from streamlit_feedback import streamlit_feedback
# trubrics 用於儲存和處理用戶反饋
import trubrics

# 密鑰和模型名稱
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_API_MODEL = st.secrets["OPENAI_API_MODEL"]

# 側邊欄
with st.sidebar:
    "[取得 OpenAI API 金鑰](https://platform.openai.com/account/api-keys)"
    "[查看源程式碼](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)"

# 設置應用的標題
st.title("📝 Chat with feedback (Trubrics)")

# 在頁面中顯示應用的說明
"""
此範例使用 [streamlit-feedback](https://github.com/trubrics/streamlit-feedback) 和
Trubrics 來收集和儲存用戶對 LLM 回應的反饋。
"""

# 初始化會話狀態中的消息列表
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "請問你需要怎樣的協助？請在每次的回覆尚為我評分。"
    }]
# 初始化會話狀態中的回應
if "response" not in st.session_state:
    st.session_state["response"] = None

# 從會話狀態中取得消息列表
messages = st.session_state.messages
# 遍歷消息列表並顯示每條消息
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 當用戶輸入新的聊天訊息時觸發
if prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 如果沒有提供 API 密鑰，顯示提示訊息
    if not OPENAI_API_KEY:
        st.info("請新增 OpenAI API 金鑰以繼續。")
        st.stop()
    # 建立 OpenAI 客戶端
    client = OpenAI(api_key=OPENAI_API_KEY)
    # 使用 OpenAI 的聊天模型生成回應
    response = client.chat.completions.create(
        model=OPENAI_API_MODEL, messages=messages
    )
    # 將回應儲存在會話狀態中
    st.session_state["response"] = response.choices[0].message.content
    # 顯示助手的回應
    with st.chat_message("assistant"):
        messages.append({
            "role": "assistant",
            "content": st.session_state["response"]
        })
        st.write(st.session_state["response"])

# 如果存在回應，收集用戶反饋
if st.session_state["response"]:
    feedback = streamlit_feedback(
        # 使用 thumbs 作為反饋類型
        feedback_type="thumbs",
        # 可選的文本標籤
        optional_text_label="[可選] 請提供解釋",
        # 為反饋設置鍵值
        key=f"feedback_{len(messages)}",
    )
    # 該應用程序將反饋記錄到 Trubrics 後端，但你可以將其發送到任何地方
    # streamlit_feedback() 的返回值僅僅是一個字典
    # 在 https://trubrics.streamlit.app/ 配置自己的帳戶
    if feedback and "TRUBRICS_EMAIL" in st.secrets:
        config = trubrics.init(
            # 初始化 Trubrics 配置
            email=st.secrets.TRUBRICS_EMAIL,
            password=st.secrets.TRUBRICS_PASSWORD,
        )
        collection = trubrics.collect(
            # 設置組件名稱
            component_name="default",
            # 設置模型名稱
            model=OPENAI_API_MODEL,
            # 設置收集到的反饋
            response=feedback,
            # 設置元數據，包括聊天記錄
            metadata={"chat": messages}
        )
        # 保存反饋到 Trubrics
        trubrics.save(config, collection)
        # 顯示提示訊息
        st.toast("反饋已記錄！", icon="📝")
