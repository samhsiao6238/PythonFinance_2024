# 導入所需庫
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.schema import Document
from langchain.schema import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.vectorstores import Chroma
import os
import requests

# 確保 Streamlit 已經設置 API 金鑰為環境變量
if "GEMINI_API_KEY" not in st.secrets:
    st.error("請在 Streamlit 配置中設置 GEMINI_API_KEY")
    st.stop()

# 從 Streamlit 的 secrets 中取得 API 金鑰
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# 確保環境變量設置正確
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
# 設置 HTTP 請求的 USER_AGENT
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 "
    "Safari/537.36"
)

# 檢查是否設置 API 金鑰
if GEMINI_API_KEY is None:
    st.error("環境變數 GEMINI_API_KEY 未設置，請檢查 .env 文件。")
    st.stop()

# 模型指定為 gemini-pro
model_name = "gemini-pro"

# 初始化 ChatGoogleGenerativeAI 模型
model = ChatGoogleGenerativeAI(model=model_name, google_api_key=GEMINI_API_KEY)

# 設置應用程序標題
st.title("Gemini API 文本生成器")

# 建立文本輸入框供用戶輸入問題
user_input = st.text_input("請輸入你的問題：")

# 當用戶點擊生成按鈕時執行的操作
if st.button("生成"):
    if not user_input:
        # 如果用戶未輸入文本，提示輸入
        st.warning("請輸入一些文本。")
    else:
        try:
            # 建立 HumanMessage 實例
            message = HumanMessage(content=user_input)

            # 使用模型生成文本
            response = model.stream([message])

            # 建立一個空的 Streamlit 元素，以便後續更新輸出
            output_placeholder = st.empty()
            generated_text = ""

            # 使用流式方式逐步顯示生成的文本
            for chunk in response:
                generated_text += chunk.content
                output_placeholder.text(generated_text)

            # 顯示成功信息，指示文本生成完成
            st.success("文本生成已完成。")

        except Exception as e:
            # 捕獲錯誤並顯示
            st.error(f"發生錯誤： {str(e)}")

# 建立網站數據加載器
headers = {"User-Agent": USER_AGENT}
response = requests.get(
    "https://blog.google/technology/ai/google-gemini-ai/",
    headers=headers
)

# 確認請求是否成功
if response.status_code != 200:
    st.error(f"無法加載數據，狀態碼: {response.status_code}")
else:
    # 加載網站數據
    text_content = response.text

    # 使用 Python 的 split 方法提取所需文本內容
    text_content_1 = text_content.split(
        "code, audio, image and video.", 1
    )[1]
    final_text = text_content_1.split(
        "Cloud TPU v5p", 1
    )[0]

    # 將提取的文本轉換為 LangChain 的 Document 格式
    docs = [
        Document(
            page_content=final_text,
            metadata={"source": "local"}
        )
    ]

    # 初始化嵌入模型
    gemini_embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )

    # 使用 Chroma 建立向量資料庫
    vectorstore = Chroma.from_documents(
        # 數據
        documents=docs,
        # 嵌入模型
        embedding=gemini_embeddings,
        # 保存數據的目錄
        persist_directory="./chroma_db"
    )

    # 從磁盤加載向量資料庫
    vectorstore_disk = Chroma(
        # 資料庫目錄
        persist_directory="./chroma_db",
        # 嵌入模型
        embedding_function=gemini_embeddings
    )

    # 建立檢索器
    retriever = vectorstore_disk.as_retriever(
        search_kwargs={"k": 1}
    )
    # 測試檢索器是否正常工作
    print(len(retriever.get_relevant_documents("MMLU")))

    # 初始化 Gemini 模型，並設置參數如溫度和 top_p
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        top_p=0.85
    )

    # 建立問答提示模板
    llm_prompt_template = """
    你是一位專業的咨詢師。
    請使用以下的上下文來回答問題。
    你的回答請使用繁體中文以及繁體中文用語。
    如果你不知道答案，就說你不知道。
    你的回覆最多不要超過五個句子，並保持答案簡潔。
    \n問題：{question}
    \n上下文：{context}
    \n答案：
    """

    # 使用 LangChain 建立 PromptTemplate
    llm_prompt = PromptTemplate.from_template(
        llm_prompt_template
    )

    # 定義格式化文件的函數
    def format_docs(docs):
        return "\n\n".join(
            doc.page_content for doc in docs
        )

    # 建立文件鏈
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | llm_prompt
        | llm
        | StrOutputParser()
    )
