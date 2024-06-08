import os
import certifi
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient

# 環境變數
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

# 連線資料庫
client = MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
db_name = "MyDatabase2024"
collection_name = "MyCollection2024"
atlas_collection = client[db_name][collection_name]
vector_search_index = "vector_index"


# 載入數據並建立向量儲存
def initialize_data():
    # Load text file
    loader = TextLoader("紅樓夢.txt")
    data = loader.load()
    # 文件分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=20
    )
    # 分割文件
    docs = text_splitter.split_documents(data)
    # 建立向量儲存
    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        collection=atlas_collection,
        index_name=vector_search_index,
    )
    return vector_search


# 檢查集合是否存在
if atlas_collection.count_documents({}) == 0:
    st.write("初始化資料並創建向量存儲...")
    vector_search = initialize_data()
else:
    st.write("已有資料，載入現有向量儲存...")
    vector_search = MongoDBAtlasVectorSearch(
        collection=atlas_collection,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        index_name=vector_search_index,
    )

# 標題
st.title("文件問答系統")

# 發問
question = st.text_input("請輸入您的問題：", "請簡述這個文本的主要內容")

# 提交
if st.button("提交問題"):
    # 初始化取回元件
    retriever = vector_search.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10, "score_threshold": 0.75},
    )
    template = """
    使用以下內容來回答最後的問題。
    如果你不知道答案，就說你不知道，不要試圖編造答案。
    {context}
    問題：{question}
    """
    custom_rag_prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    # 取回相關文件
    documents = retriever.get_relevant_documents(question)
    # 取回答案
    answer = rag_chain.invoke(question)
    st.subheader("回答：")
    st.write(answer)

    # 顯示結果
    # st.subheader("相關文件：")
    # for doc in documents:
    #     st.write(doc.page_content)

    # # 可顯示原文件案
    # with st.expander("查看源文件"):
    #     pprint.pprint(documents)
