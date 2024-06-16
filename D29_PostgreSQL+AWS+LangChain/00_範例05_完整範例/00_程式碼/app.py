import streamlit as st
from PyPDF2 import PdfReader
from langchain.vectorstores.pgvector import PGVector
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings
from langchain.document_loaders import S3FileLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import YoutubeLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.memory import PostgresChatMessageHistory
import boto3
import tempfile
import time
import hashlib
import secrets
import os
from dotenv import load_dotenv
import logging

# 載入環境變數
load_dotenv()
# 注意，`environ.get` 或 `os.getenv` 兩者在本質上是有差異的
# 但我偏向程式碼整潔，所以在程序一開始之處就載入 `load_dotenv()`
# 這樣的載入方式使用 `environ.get` 或 `os.getenv` 並無差異
PGVECTOR_DRIVER = os.getenv("PGVECTOR_DRIVER")
PGVECTOR_USER = os.getenv("PGVECTOR_USER")
PGVECTOR_PASSWORD = os.getenv("PGVECTOR_PASSWORD")
PGVECTOR_HOST = "localhost"
PGVECTOR_PORT = "5432"
PGVECTOR_DATABASE = "mydatabase"

logging.getLogger("botocore").setLevel(logging.ERROR)


def debug_01():
    # 檢查資料庫的 URI 是否正確
    CONNECTION_STRING = f"://{PGVECTOR_USER}:{PGVECTOR_PASSWORD}@{PGVECTOR_HOST}:{PGVECTOR_PORT}/{PGVECTOR_DATABASE}"
    # 確保正確打印連接字串，便於檢查
    print(f"CONNECTION_STRING: {CONNECTION_STRING}")


def styled_header(text):
    header_html = f"""
    <div style="background-color:#4CAF50;text-align:center;padding:10px">
    <h1 style="color:white;text-align:center;">{text}</h1>
    </div>
    """
    return header_html


def styled_subheader(
    text,
    font_size="24px",
    color="#8A2BE2",
    background_color="#f0e5ff"
):
    subheader_html = f"""
    <div style="box-shadow:0 2px 10px #ddd; padding: 5px;"
    " background-color: {background_color};"
    " border-radius: 5px; margin: 10px 0; text-align: center;">
        <h3 style="color: {color}; font-size: {font_size};"
        " margin: 0;">{text}</h3>
    </div>
    """
    return subheader_html


def generate_session_id():
    t = int(time.time() * 1000)
    r = secrets.randbelow(1000000)
    return hashlib.md5(
        bytes(str(t) + str(r), "utf-8"), usedforsecurity=False
    ).hexdigest()


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            # text += page.extract_text()
            # 改用 page_text，後面再傳回
            page_text = page.extract_text()
            # 過濾掉 NUL 字串
            if page_text:
                text += page_text.replace('\x00', '')
    return text


def get_text_chunks(text):
    # 確保在分割文本塊前過濾掉 NUL 字串
    cleaned_text = text.replace('\x00', '')
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        chunk_size=512,
        chunk_overlap=103,
        length_function=len,
    )
    # chunks = text_splitter.split_text(text)
    chunks = text_splitter.split_text(cleaned_text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        # 預設是 `-2`，這裡改一下
        region_name="us-east-1"
    )
    try:
        if text_chunks is None:
            return PGVector(
                connection_string=CONNECTION_STRING,
                embedding_function=embeddings,
            )
        return PGVector.from_texts(
            texts=text_chunks,
            embedding=embeddings,
            connection_string=CONNECTION_STRING
        )
    except Exception as e:
        # 原本的腳本是引發錯誤
        # raise e
        # 改為輸出錯誤看一下
        print(f'取得向量儲存發生錯誤：{e}')


def get_bedrock_llm(selected_llm):
    print(f"[INFO] Selected LLM is : {selected_llm}")
    if selected_llm in [
        "anthropic.claude-v2",
        "anthropic.claude-v1",
        "anthropic.claude-instant-v1",
    ]:
        llm = Bedrock(
            model_id=selected_llm,
            model_kwargs={"max_tokens_to_sample": 4096}
        )

    elif selected_llm in [
        "amazon.titan-tg1-large",
        "amazon.titan-text-express-v1",
        "amazon.titan-text-lite-v1",
    ]:
        llm = Bedrock(
            model_id=selected_llm,
            model_kwargs={
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1,
            },
        )
    else:
        raise ValueError(f"Unsupported LLM: {selected_llm}")

    return llm


def get_conversation_chain(vectorstore, selected_llm):
    # 註解掉
    # llm = Bedrock(
    #     model_id="anthropic.claude-instant-v1",
    #     region_name="us-west-2"
    # )
    llm = get_bedrock_llm(selected_llm)
    _connection_string = CONNECTION_STRING.replace(
        "+psycopg2", "").replace(":5432", "")
    message_history = PostgresChatMessageHistory(
        connection_string=_connection_string, session_id=generate_session_id()
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        return_source_documents=True,
        return_messages=True,
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, retriever=vectorstore.as_retriever(), memory=memory
    )
    return conversation_chain


def color_text(text, color="black"):
    return f'<span style="color:{color}">{text}</span>'


bot_template = "🤖 BOT : {0}"
user_template = "👤 USER : {0}"


def handle_userinput(user_question):
    bot_template = "🤖 BOT : {0}"
    user_template = "👤 USER : {0}"
    try:
        response = st.session_state.conversation({"question": user_question})
        st.markdown(
            color_text(
                user_template.format(response["question"]),
                color="blue"
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            color_text(
                bot_template.format(response["answer"]),
                color="green"
            ),
            unsafe_allow_html=True,
        )
        print("Response", response)
    except ValueError as e:
        st.write(e)
        st.write("😞 抱歉，請換個方式再問一次。")
        return
    st.session_state.chat_history = response["chat_history"]
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(
                color_text(
                    user_template.format(message.content),
                    color="blue"
                ),
                unsafe_allow_html=True,
            )

        else:
            st.markdown(
                color_text(
                    bot_template.format(message.content),
                    color="green"
                ),
                unsafe_allow_html=True,
            )


def main():
    # Updated header styling
    st.markdown(
        styled_header(
            "Unified AI Q&A: Harnessing pgvector, Amazon Aurora"
            " & Amazon Bedrock 📚🦜"
        ),
        unsafe_allow_html=True,
    )

    options = [
        "📄 PDFs",
        "☁️ S3 Bucket",
        "📺 Youtube",
        "📑 CSV", "🖼️ PPT",
        "📝 Word"
    ]
    # 使用單選按鈕而不是選擇框
    st.markdown(
        styled_subheader("📌 Select a source 📌"),
        unsafe_allow_html=True
    )
    selected_source = st.radio("", options)

    # 添加 LLM 選單元件
    st.markdown(
        styled_subheader("🤖 Select the LLM 🤖"),
        unsafe_allow_html=True
    )
    llm_options = [
        "anthropic.claude-v2",
        "anthropic.claude-instant-v1",
        "amazon.titan-tg1-large",
        "amazon.titan-text-express-v1",
        "amazon.titan-text-lite-v1",
    ]

    selected_llm = st.radio("Choose an LLM", options=llm_options)

    # PDF
    if selected_source == "📄 PDFs":
        pdf_docs = st.file_uploader(
            "📥 Upload your PDFs here:",
            type="pdf",
            accept_multiple_files=True
        )
        if st.button("🔄 Process"):
            with st.spinner("🔧 Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                if vectorstore is None:
                    st.write("Failed to initialize vector store.")
                    return
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, selected_llm
                )
    elif selected_source == "☁️ S3 Bucket":
        s3_client = boto3.client("s3")
        # 這些物件儲存在 aurora-genai-2023 儲存桶中。輸入適當的儲存桶名稱
        response = s3_client.list_objects_v2(
            # 將儲存桶名稱變更為自己的儲存桶名稱
            Bucket="aurora-genai-2023",
            Prefix="documentEmbeddings/"
        )
        document_keys = [
            obj["Key"].split("/")[1]
            for obj in response["Contents"]
        ][1:]
        user_input = st.selectbox(
            "Select an S3 document and click on 'Process'",
            document_keys
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                prefix = "documentEmbeddings/" + user_input
                loader = S3FileLoader("aurora-genai-2023", prefix)
                docs = loader.load()
                for i in docs:
                    text_chunks = get_text_chunks(i.page_content)
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.write("Failed to initialize vector store.")
                        return
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, selected_llm
                )
    elif selected_source == "📑 CSV":
        csv_docs = st.file_uploader(
            "Upload your CSV here and click on 'Process'",
            type="csv",
            accept_multiple_files=False,
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(csv_docs.getvalue())
                    tmp_file_path = tmp_file.name
                loader = CSVLoader(
                    file_path=tmp_file_path,
                    encoding="utf-8",
                    csv_args={"delimiter": ","},
                )
                docs = loader.load()
                for i in docs:
                    text_chunks = get_text_chunks(i.page_content)
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.write("Failed to initialize vector store.")
                        return
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, selected_llm
                )
    elif selected_source == "📺 Youtube":
        user_input = st.text_input("輸入 YouTube 連結並點擊「Process」")
        if st.button("Process"):
            with st.spinner("Processing"):
                loader = YoutubeLoader.from_youtube_url(user_input)
                transcript = loader.load()
                for i in transcript:
                    text_chunks = get_text_chunks(i.page_content)
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.write("無法初始化向量儲存。")
                        return
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, selected_llm
                )

    elif selected_source == "🖼️ PPT":
        ppt_docs = st.file_uploader(
            "在此上傳您的 PPT，然後按一下「Process」",
            type=["ppt", "pptx"],
            accept_multiple_files=False,
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(ppt_docs.getvalue())
                    tmp_file_path = tmp_file.name
                loader = UnstructuredPowerPointLoader(tmp_file_path)
                docs = loader.load()
                for i in docs:
                    text_chunks = get_text_chunks(i.page_content)
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.write("無法初始化向量儲存。")
                        return
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, selected_llm
                )

    elif selected_source == "📝 Word":
        word_docs = st.file_uploader(
            "在此處上傳您的 Word 文件，然後按一下「Process」",
            type=["docx"],
            accept_multiple_files=False,
        )
        if st.button("Process"):
            with st.spinner("Processing"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(word_docs.getvalue())
                    tmp_file_path = tmp_file.name
                loader = Docx2txtLoader(tmp_file_path)
                docs = loader.load()
                for i in docs:
                    text_chunks = get_text_chunks(i.page_content)
                    vectorstore = get_vectorstore(text_chunks)
                    if vectorstore is None:
                        st.write("無法初始化向量儲存。")
                        return
                st.session_state.conversation = get_conversation_chain(
                    vectorstore, selected_llm
                )

    st.sidebar.header("🗣️ 與機器人聊天")
    user_question = st.sidebar.text_input("💬 詢問有關你所提供數據的問題：")
    if user_question:
        handle_userinput(user_question)

    if "conversation" not in st.session_state:
        st.session_state.conversation = get_conversation_chain(
            get_vectorstore(None), selected_llm
        )
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None


# 輸入資料庫名稱
if __name__ == "__main__":
    # 若在 `__main__` 中載入則必須使用 `environ.get` 來讀取並寫入環境參數
    # load_dotenv()

    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver=PGVECTOR_DRIVER,
        user=PGVECTOR_USER,
        password=PGVECTOR_PASSWORD,
        host=PGVECTOR_HOST,
        port=PGVECTOR_PORT,
        database=PGVECTOR_DATABASE,
    )

    main()
