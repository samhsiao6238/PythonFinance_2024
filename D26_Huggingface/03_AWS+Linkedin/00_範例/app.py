import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_aws import BedrockLLM
# 導入自訂庫
from third_parties.linkedin import scrape_linkedin_profile
# 導入自訂庫中的 lookup，並使用別名 lookup_agent
from agents.linkedin_lookup_agent import lookup as lookup_agent

# 加載環境變量
load_dotenv()


def get_llm():
    bedrock_llm = BedrockLLM(
        # 模型
        model_id="anthropic.claude-v2",
        # 區域
        region_name=os.getenv("AWS_REGION"),
        # 模型參數
        model_kwargs={
            "temperature": 0.1,
            "max_tokens_to_sample": 4096},
    )
    return bedrock_llm


def ice_break_with(name: str):
    # 調用自訂函數
    linkedin_profile_url = lookup_agent(name=name)
    if not linkedin_profile_url:
        return "未能找到該人的 LinkedIn 資料。"

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url
    )
    if not linkedin_data:
        return "未能抓取該人的 LinkedIn 資料。"

    summary_template = """
    鑑於有關某人的 LinkedIn 資訊 {information}，請創建以下內容，並用繁體中文回答：
    1. 先介紹他的名字
    2. 簡短總結
    2. 關於他的兩個有趣的事實
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )

    llm = get_llm()
    chain = summary_prompt_template | llm

    result = chain.invoke({"information": linkedin_data})
    return result


def main():
    st.title("建立連結 💼✨")
    st.write("使用 Amazon Bedrock 和 LangChain 根據社群媒體資料建立摘要的應用程式。 🚀")

    st.sidebar.header("🔎 輸入此人的詳細信息")
    name = st.sidebar.text_input("名字 (e.g., 'Andy Jassy Amazon'):")

    if st.sidebar.button("取得摘要"):
        with st.spinner("取得 LinkedIn 數據並建立摘要... 🔄"):
            result = ice_break_with(name)
        st.subheader("摘要和一些有趣的事實 📝")
        st.write(result)
        st.success("摘要生成成功！ 👍")

        st.markdown(
            "<h3 style='text-align: center; font-size: 20px;'>"
            " To know more about Amazon Bedrock, visit"
            " <a href='https://aws.amazon.com/bedrock/'"
            " target='_blank'>here</a> </h3>",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <style>
            body {
                color: #4f4f4f;
                background-color: #F5F5F5;
            }
            .stButton>button {
                color: #4f4f4f;
                background-color: #FFD700;
                border-radius: 30px;
                padding: 10px 20px;
                font-size: 1.2em;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    load_dotenv()
    main()
