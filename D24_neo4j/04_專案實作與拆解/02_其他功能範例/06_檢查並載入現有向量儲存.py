import os
import pprint
import certifi
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pymongo import MongoClient

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

# Connect to MongoDB Atlas
client = MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
db_name = "MyDatabase2024"
collection_name = "MyCollection2024"
atlas_collection = client[db_name][collection_name]
vector_search_index = "vector_index"


# Function to load data and create vector store
def initialize_data():
    # Load PDF
    loader = PyPDFLoader("論文01.pdf")
    data = loader.load()
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=20
    )
    docs = text_splitter.split_documents(data)
    # Create vector store
    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        collection=atlas_collection,
        index_name=vector_search_index,
    )
    return vector_search


# Check if the collection is empty and initialize data if necessary
if atlas_collection.count_documents({}) == 0:
    st.write("初始化資料並創建向量存儲...")
    vector_search = initialize_data()
else:
    st.write("載入現有向量儲存...")
    vector_search = MongoDBAtlasVectorSearch(
        collection=atlas_collection,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        index_name=vector_search_index,
    )

# Streamlit interface
st.title("文檔問答系統")

# User input for question
question = st.text_input("請輸入您的問題：", "簡述這篇論文的研究方法")

# Button to trigger query
if st.button("提交問題"):
    # Initialize retriever and other components
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

    # Retrieve relevant documents and get the answer
    documents = retriever.get_relevant_documents(question)
    answer = rag_chain.invoke(question)

    # Display results
    st.subheader("相關文檔：")
    for doc in documents:
        st.write(doc.page_content)

    st.subheader("回答：")
    st.write(answer)

    # Optionally display source documents
    with st.expander("查看源文檔"):
        pprint.pprint(documents)
