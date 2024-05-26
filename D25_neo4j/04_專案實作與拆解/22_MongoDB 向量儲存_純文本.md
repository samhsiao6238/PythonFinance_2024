# 向量索引

_讀取 TXT 並建立向量索引系統_

<br>

## 說明

1. 不僅限於讀取 PDF 文件，任何能夠 `轉換為向量嵌入（vector embeddings）` 的數據類型都可以使用 `向量索引` 和 `向量搜索` 技術。

<br>

## 可用類型

1. PDF 文件：通過類似 `PyPDFLoader` 的工具，可以將 PDF 文件的內容加載並轉換為向量嵌入。

<br>

2. 純文本文件：可以直接通過嵌入模型轉換為向量嵌入。

<br>

3. 圖片和多媒體數據：可以通過圖像嵌入模型轉換為向量，這在圖像搜索、相似圖像查找等應用中非常有用。

<br>

4. 結構化數據：結構化數據如數據庫記錄，可以通過嵌入模型轉換為向量，用於相似記錄檢索。

<br>

5. 音頻和視頻數據：音頻和視頻數據可以通過相應的模型轉換為向量，實現多媒體數據的相似性檢索。

<br>

6. 網頁和 HTML：網頁內容可以通過文本處理和嵌入技術轉換為向量，用於相似網頁檢索。

<br>

## 範例：讀取純文本文件

1. 以下範例展示如何加載純文本文件並將其轉換為向量嵌入，然後存儲在 MongoDB 的向量索引中。

<br>

2. 程式碼。

    ```python
    import os
    import pymongo
    import pprint
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
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
    st.title("文檔問答系統")

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

        # 顯示結果
        st.subheader("回答：")
        st.write(answer)

        # 相關文檔 
        # st.subheader("相關文檔：")
        # for doc in documents:
        #     st.write(doc.page_content)

        # 可顯示原文檔案
        # with st.expander("查看源文檔"):
        #     pprint.pprint(documents)
    ```

<br>

## 互動

_可透過詢問各種問題來測試_

<br>

1. `《紅樓夢》中石頭的象徵意義是什麼？`

    ![](images/img_40.png)

<br>

2. `《紅樓夢》的時代背景是什麼？`

    ![](images/img_41.png)

<br>

___

_END_