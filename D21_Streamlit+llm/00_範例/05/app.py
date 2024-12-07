import streamlit as st
# 使用 langchain_openai 的 ChatOpenAI
from langchain_openai import ChatOpenAI
# 引入 LangChain 的 PromptTemplate 模組，用於建立 `提示模板`
from langchain.prompts import (
    PromptTemplate,
)

# 密鑰和模型名稱
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_API_MODEL = st.secrets["OPENAI_API_MODEL"]

# 標題
st.title("🦜🔗 Langchain - Blog Outline Generator App")


# 自訂函數：生成大綱
def generate_outline(topic):
    # 實例化語言模型對象
    llm = ChatOpenAI(
        model_name=OPENAI_API_MODEL,
        openai_api_key=OPENAI_API_KEY
    )
    # 建立提示模板
    template = "作為經驗豐富的資料科學家和學者，請你為有關 {topic} 的主題製定演講大綱"
    prompt = PromptTemplate(
        # 指定模板中使用的變數名稱
        input_variables=["topic"],
        # 提供模板字串
        template=template,
    )
    # 格式化提示，將主題插入到模板中
    prompt_query = prompt.format(topic=topic)
    # 運行語言模型，生成回應
    response = llm.invoke(prompt_query)

    # 取得回應：直接訪問 response 的 content 屬性
    content = response.content
    # 調用自訂函數將回應解析並為更易於理解的自然語言格式
    formatted_response = format_response(content)

    # 顯示結果
    return st.info(formatted_response)


def format_response(response):
    """
    將模型的回應解析並格式化為易於閱讀的自然語言。
    """
    sections = response.split("\n\n")
    formatted_response = ""

    for section in sections:
        if section.startswith("Blog Title:"):
            formatted_response += f"### {section}\n"
        elif section.startswith("Introduction"):
            formatted_response += f"**{section}**\n"
        elif section.startswith("Section"):
            formatted_response += f"#### {section}\n"
        elif section.startswith("Conclusion"):
            formatted_response += f"**{section}**\n"
        elif section.startswith("Call to Action"):
            formatted_response += f"**{section}**\n"
        else:
            formatted_response += f"{section}\n"

    return formatted_response


# 建立名為 "myform" 的表單，用於接收用戶輸入
with st.form("myform"):
    # 在表單內添加一個文本輸入框，讓用戶輸入主題
    topic_text = st.text_input("請輸入主題關鍵字：", "")
    # 在表單內添加一個提交按鈕
    submitted = st.form_submit_button("提交")
    if not OPENAI_API_KEY:
        # 如果沒有提供 API 密鑰，顯示提示訊息
        st.info("請新增 OpenAI API 金鑰以繼續。")
    elif submitted:
        # 調用自訂函數，生成博客大綱
        generate_outline(topic_text)
