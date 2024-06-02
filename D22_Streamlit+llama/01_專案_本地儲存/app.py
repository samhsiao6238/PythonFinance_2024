import os
import nest_asyncio
import streamlit as st
from llama_index.readers.file import UnstructuredReader
from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.agent.openai import OpenAIAgent
from pathlib import Path

# 設置 OpenAI API 密鑰
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
nest_asyncio.apply()

st.title("UBER 10-K Chatbot")


# 步驟一：下載並解析數據
def download_and_parse_data():
    # 添加檢查是否存在數據
    if not os.path.exists("data/UBER.zip"):
        if not os.path.exists("data"):
            os.mkdir("data")
            os.system(
                "wget 'https://www.dropbox.com/"
                "s/948jr9cfs7fgj99/UBER.zip?dl=1' "
                "-O data/UBER.zip"
            )
            os.system("unzip data/UBER.zip -d data")
    years = [2022, 2021, 2020, 2019]
    loader = UnstructuredReader()
    doc_set = {}
    all_docs = []
    for year in years:
        year_docs = loader.load_data(
            file=Path(f"./data/UBER/UBER_{year}.html"), split_documents=False
        )
        for d in year_docs:
            d.metadata = {"year": year}
        doc_set[year] = year_docs
        all_docs.extend(year_docs)
    return years, doc_set


# 步驟二：設置向量索引
# 將解析後的文件數據轉換為向量並存儲在本地磁碟中的指定目錄內
# 向量索引是存儲在各年度對應的目錄中，如 ./storage/2022、./storage/2021 等
def setup_vector_indices(years, doc_set):
    Settings.chunk_size = 512
    Settings.chunk_overlap = 64
    Settings.llm = OpenAI(
        model=st.secrets["OPENAI_MODEL"],
        # temperature=0.7
    )
    Settings.embed_model = OpenAIEmbedding(
        # model="text-embedding-ada-002"
        model=st.secrets["OPENAI_EMBEDDING_MODEL"]
    )
    # 檢查索引是否存在
    index_set = {}
    for year in years:
        persist_dir = f"./storage/{year}"
        vector_store_path = os.path.join(persist_dir, "vector_store.json")

        if os.path.exists(vector_store_path):
            st.write(
                f"Vector index for year {year} "
                "already exists. Skipping creation."
            )
            continue

        storage_context = StorageContext.from_defaults()
        cur_index = VectorStoreIndex.from_documents(
            doc_set[year], storage_context=storage_context
        )
        index_set[year] = cur_index
        storage_context.persist(persist_dir=persist_dir)
    return index_set


# 步驟三：載入向量索引
def load_vector_indices(years):
    index_set = {}
    for year in years:
        try:
            storage_context = StorageContext.from_defaults(
                persist_dir=f"./storage/{year}"
            )
            cur_index = load_index_from_storage(storage_context)
            index_set[year] = cur_index
        except ValueError as e:
            st.warning(f"Could not load index for year {year}: {e}")
    return index_set


# 步驟四：設置子問題查詢引擎
def setup_sub_question_query_engine(index_set, years):
    individual_query_engine_tools = [
        QueryEngineTool(
            query_engine=index_set[year].as_query_engine(),
            metadata=ToolMetadata(
                name=f"vector_index_{year}",
                description=(
                    "useful for when you want to answer queries "
                    f"about the {year} SEC 10-K for Uber"
                ),
            ),
        )
        for year in years
    ]
    query_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=individual_query_engine_tools
    )
    return query_engine, individual_query_engine_tools


# 步驟五：設置聊天機器人代理
def setup_agent(query_engine, individual_query_engine_tools):
    query_engine_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="sub_question_query_engine",
            description=(
                "useful for when you want to answer "
                "queries that require analyzing multiple "
                "SEC 10-K documents for Uber"
            ),
        ),
    )
    tools = individual_query_engine_tools + [query_engine_tool]
    agent = OpenAIAgent.from_tools(tools, verbose=True)
    return agent


years, doc_set = download_and_parse_data()
# 這一步確保索引被重新生成並持久化
index_set = setup_vector_indices(years, doc_set)
index_set = load_vector_indices(years)
query_engine, individual_query_engine_tools = setup_sub_question_query_engine(
    index_set, years
)
agent = setup_agent(query_engine, individual_query_engine_tools)

# 聊天機器人互動循環
user_input = st.text_input("User:", "")
if user_input:
    try:
        response = agent.chat(user_input)
        st.write(f"Agent: {response}")
    except Exception as e:
        st.error(f"發生錯誤：{e}")
if st.button("測試範例問題"):
    response = agent.chat(
        "What were some of the biggest risk factors in 2020 for Uber?"
    )
    st.write(f"Agent: {response}")
