# 實作網站文本嵌入

_以下步驟涵蓋了新聞爬取、嵌入向量生成、儲存到 MongoDB、以及基於向量的相似新聞檢索，這些步驟可實現一個基於向量嵌入的新聞推薦系統，讓用戶在閱讀完某篇新聞後，獲得相關的新聞推薦，提升閱讀體驗。_

<br>

## 步驟說明

1. 安裝必要庫。

    ```bash
    pip install requests beautifulsoup4 openai pymongo
    ```

<br>

2. 爬取 Yahoo 新聞，先從 Yahoo 新聞中爬取有關 `中華職棒中信兄弟` 的新聞。

    ```python
    import requests
    from bs4 import BeautifulSoup

    def fetch_yahoo_news(query):
        search_url = f"https://tw.news.yahoo.com/search?p={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        
        # 搜尋新聞標題和鏈接
        for item in soup.select('li[class*="StreamMegaItem"]'):
            title_element = item.select_one('h3[class*="Mb"] a[class*="Fw"]')
            if title_element:
                title = title_element.get_text()
                link = title_element['href']
                articles.append({'title': title, 'link': link})
        
        return articles

    news_articles = fetch_yahoo_news("中華職棒中信兄弟")
    for article in news_articles:
        print(article['title'])
        # 若需要連結：article['link']
    ```

    _結果_

    ```bash
    高國慶引退賽延後開打 賽前白板暖心留言
    傳承KANO精神 校友官大元交棒嘉大棒球隊伍立辰
    魔鷹開轟單場5打點大爆發！雄鷹大勝兄弟
    猛登7局失1分優質先發 助兄弟擊敗獅 (圖)
    中職週報》財務問題有中職球隊敢網羅？黃勇傳被統一開除隔天與經紀公司解約
    中職新莊戰 中信兄弟猛登先發 (圖)
    富邦悍將擊敗中信兄弟 江國豪勝投 (圖)
    中職新莊戰 中信兄弟先馳得點 (圖)
    中職新莊戰 中信兄弟楊祥禾敲安 (圖)
    中信兄弟延長賽不敵富邦悍將 吳俊偉吞敗 (圖)
    中職新莊戰 中信兄弟陳俊秀敲安帶打點 (圖)
    中職／王威晨明星賽破10萬票暫居人氣王 中信兄弟守備位置包辦8個
    王正棠再見安打 富邦悍將擊敗中信兄弟 (圖)
    中職新莊戰 富邦悍將完封中信兄弟 (圖)
    3隊大亂鬥兄弟勝出靠火力 統一獅折損大將
    中職》首位突破10萬票！ 中信兄弟王威晨暫居人氣王寶座
    擋不住兄弟攻勢 統一獅野手林佳緯登板投球 (圖)
    統一獅高國慶引退賽哭了！ 揮手向球迷淚別｜#鏡新聞
    中職明星賽王威晨人氣王 葉保弟排外野前三
    中職》去年突破760萬票！今年中職明星賽將進軍臺北大巨蛋 球迷投票14日中午12點正式展開
    ```

<br>

3. 配置 API Key 和 MongoDB 超連結。

    ```python
    import os
    import certifi
    from pymongo import MongoClient
    import streamlit as st

    # 設置環境變數
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]
    ```

<br>

4. 建立 MongoDB 連線對象。

    ```python
    client = MongoClient(
        ATLAS_CONNECTION_STRING,
        tlsCAFile=certifi.where()
    )
    # 選擇特定的資料庫和集合
    db_name = "MyDatabase2024"
    collection_name = "MyCollection2024"
    atlas_collection = client[db_name][collection_name]
    vector_search_index = "vector_index"
    ```

<br>

5. 調用爬蟲並生成嵌入向量，並將其儲存到 MongoDB。

    ```python
    from langchain.docstore.document import Document
    from langchain_openai import OpenAIEmbeddings

    def process_news_and_store_embeddings(query):
        news_articles = fetch_yahoo_news(query)
        
        news_documents = []
        embedding_model = OpenAIEmbeddings(disallowed_special=())

        for article in news_articles:
            embeddings = embedding_model.embed_documents([article["title"]])
            if embeddings:
                doc = Document(page_content=article["title"], metadata={"title": article["title"]})
                news_documents.append(doc)
            else:
                print(f"對文章生成 Embedding 時出錯：{article['title']}")

        if news_documents:
            atlas_collection.insert_many(
                [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in news_documents]
            )
            print("嵌入向量已儲存到 MongoDB Atlas。")
        else:
            print("未能生成嵌入向量。")
    ```

<br>

6. 調用爬取儲存函數，爬取與 `中信兄弟` 相關的新聞並儲存嵌入向量。

    ```python
    query = "中信兄弟"
    process_news_and_store_embeddings(query)
    ```

<br>

7. 從 MongoDB 載入文件，並使用這些文件建立 `向量搜索索引`。

    ```python
    from langchain_mongodb import MongoDBAtlasVectorSearch

    documents = []
    for doc in atlas_collection.find():
        if "page_content" in doc:
            documents.append(
                Document(page_content=doc["page_content"], metadata={})
            )

    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        collection=atlas_collection,
        index_name=vector_search_index,
    )
    ```

<br>

8. 相似度查詢。

    ```python
    query_text = "中信兄弟最近的比賽表現如何？"
    results = vector_search.similarity_search(query_text)
    print('\n相似度查詢：')
    pprint.pprint(results)
    ```

<br>

9. 定義 RAG 鏈，用於基於檢索到的文件生成回答。

    ```python
    from langchain.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import ChatOpenAI

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
    ```

<br>

10. 提問並基於檢索到的相關文件生成回答，並處理可能的錯誤。

    ```python
    # 提問
    question = "中信兄弟最近比賽的表現如何？"
    print(f'\n提問：{question}')
    # 取得相關文件
    documents = retriever.get_relevant_documents(question)
    # 輸出
    # pprint.pprint(documents)

    try:
        formatted_docs = format_docs(documents)
        # 輸出
        # print(f"Formatted documents: {formatted_docs}")
        # 確保上下文是字串
        if isinstance(formatted_docs, str) and isinstance(question, str):
            # 是字串就直接提問
            answer = rag_chain.invoke(question)
            print("\n回答：" + answer)
        else:
            print("錯誤：格式化文件或問題不是字串。")
    except Exception as e:
        print(f"進行 RAG chain invoke 時發生錯誤：{e}")
    ```

<br>

11. 運行結果，可觀察到在相似度查詢中無法得到文件，但是提問是可以得到答案的。

    ```bash
    嵌入向量已儲存到 MongoDB Atlas。

    相似度查詢：中信兄弟最近比賽的表現如何？
    []

    提問：中信兄弟最近比賽的表現如何？

    回答：中信兄弟最近的比賽表現並不理想，他們在一些比賽中遭遇了慘敗，被對手猛攻並且失分較多。在一些比賽中，他們的投手表現也不盡如人意。然而，在一些比賽中，兄弟隊的火力攻勢表現出色，取得了勝利。总体来说，中信兄弟的表现有起有伏。
    ```

<br>

12. 換一個問法，可觀察到不同的狀況，相似度查詢可得到部分文本，但提問則無法得到較為精準的答案。

    ```bash
    嵌入向量已儲存到 MongoDB Atlas。

    相似度查詢：中信兄弟近日戰績？
    [Document(page_content='猛登7局失1分優質先發 助兄弟擊敗獅 (圖)', metadata={'_id': {'$oid': '66545c3104d5609d59da77d1'}}),
    Document(page_content='中職／兄弟慘敗…雄鷹18安16分猛攻 寫3大隊史紀錄', metadata={'_id': {'$oid': '66545c3104d5609d59da77d5'}}),
    Document(page_content='中職／單局遭「完全打擊」、潘威倫3.2局失7分敗 張志豪雙響率兄弟奪勝', metadata={'_id': {'$oid': '66545c3104d5609d59da77cb'}}),
    Document(page_content='中職》首位突破10萬票！ 中信兄弟王威晨暫居人氣王寶座', metadata={'_id': {'$oid': '66545c3104d5609d59da77d7'}})]

    提問：中信兄弟近日戰績？

    回答：我不知道中信兄弟近日的戰績。
    ```

<br>

## 完成

1. 完整程式碼。

    ```python
    import requests
    from bs4 import BeautifulSoup
    import os
    import certifi
    from pymongo import MongoClient
    import streamlit as st
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_mongodb import MongoDBAtlasVectorSearch
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain.prompts import PromptTemplate
    import pprint
    from langchain.docstore.document import Document

    # 配置 OpenAI API Key 和 MongoDB 超連結
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

    # 建立 MongoDB 連線對象
    client = MongoClient(
        ATLAS_CONNECTION_STRING,
        tlsCAFile=certifi.where()
    )
    # 資料庫、集合
    db_name = "MyDatabase2024"
    collection_name = "MyCollection2024"
    # 連線指定的資料庫與集合
    atlas_collection = client[db_name][collection_name]
    # 向量搜尋名稱
    vector_search_index = "vector_index"

    # 爬取 Yahoo 新聞
    def fetch_yahoo_news(query):
        search_url = f"https://tw.news.yahoo.com/search?p={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        # 搜尋新聞標題和鏈接
        for item in soup.select('li[class*="StreamMegaItem"]'):
            title_element = item.select_one('h3[class*="Mb"] a[class*="Fw"]')
            if title_element:
                title = title_element.get_text()
                link = title_element['href']
                articles.append({'title': title, 'link': link})

        return articles

    # 爬取新聞並生成生成嵌入向量
    def process_news_and_store_embeddings(query):
        news_articles = fetch_yahoo_news(query)
        
        news_documents = []
        embedding_model = OpenAIEmbeddings(disallowed_special=())

        # 遍歷
        for article in news_articles:
            # 輸出
            # print(f"文章：{article['title']}")
            embeddings = embedding_model.embed_documents([article["title"]])
            if embeddings:
                doc = Document(page_content=article["title"], metadata={"title": article["title"]})
                news_documents.append(doc)
            else:
                print(f"對文章生成 Embedding 時出錯：{article['title']}")

        # 儲存到 MongoDB
        if news_documents:
            atlas_collection.insert_many(
                # 列表生成
                [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in news_documents]
            )
            print("嵌入向量已儲存到 MongoDB Atlas。")
        else:
            print("未能生成嵌入向量。")

    # 執行爬取和儲存
    query = "中信兄弟"
    process_news_and_store_embeddings(query)

    # 從 MongoDB 載入數據並進行相似度搜索
    documents = []
    for doc in atlas_collection.find():
        if "page_content" in doc:
            documents.append(
                Document(page_content=doc["page_content"], metadata={})
            )

    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        collection=atlas_collection,
        index_name=vector_search_index,
    )

    # 相似度查詢
    query_text = "中信兄弟最近的比賽表現如何？"
    results = vector_search.similarity_search(query_text)
    print(f'\n相似度查詢：{query_text}')
    pprint.pprint(results)

    # 定義 RAG（檢索增強生成）鏈
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
    # 提問
    question = "中信兄弟最近比賽的表現如何？"
    print(f'\n提問：{question}')
    # 取得相關文件
    documents = retriever.get_relevant_documents(question)
    # 輸出
    # pprint.pprint(documents)

    try:
        formatted_docs = format_docs(documents)
        # 輸出
        # print(f"Formatted documents: {formatted_docs}")
        # 確保上下文是字串
        if isinstance(formatted_docs, str) and isinstance(question, str):
            # 是字串就直接提問
            answer = rag_chain.invoke(question)
            print("\n回答：" + answer)
        else:
            print("錯誤：格式化文件或問題不是字串。")
    except Exception as e:
        print(f"進行 RAG chain invoke 時發生錯誤：{e}")
    ```

<br>

___

_END_
