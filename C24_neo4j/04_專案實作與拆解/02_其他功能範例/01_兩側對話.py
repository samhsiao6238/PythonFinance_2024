import streamlit as st
from streamlit_chat import message  # 引入 message 函數


# 自訂一個寫入訊息的函數，參數有：角色、內容，並預設會儲存
def write_message(role, content, save=True):
    # 儲存
    if save:
        # 依據傳入的角色將訊息寫入 session_state
        st.session_state.messages.append({"role": role, "content": content})

    # 根據角色顯示消息
    key = f"{role}_{len(st.session_state.messages)}"
    if role == "user":
        # 用戶消息，對齊右側
        message(content, is_user=True, key=key)
    else:
        # 助手消息，對齊左側
        message(content, is_user=False, key=key)


# 初始化消息列表
if "messages" not in st.session_state:
    st.session_state.messages = []

# 測試消息
write_message("user", "哈囉，你好嗎？")
write_message("assistant", "嗨～我很好，謝謝。")

# 顯示所有消息
for index, msg in enumerate(st.session_state.messages):
    key = f"{msg['role']}_{index}"
    message(msg["content"], is_user=(msg["role"] == "user"), key=key)
