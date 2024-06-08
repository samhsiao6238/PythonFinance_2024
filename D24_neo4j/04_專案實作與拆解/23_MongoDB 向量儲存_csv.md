# 向量儲存 `csv`

_讀取 CSV 並建立向量索引系統，這是 `結構化` 數據的範疇_

<br>

## 結構化數據

1. 固定格式：結構化數據易於搜索和分析是因為數據由明確的行和列所組織，每 `行 row` 表示一個記錄，每 `列 column` 表示一個屬性或特徵。

2. 易於檢索和分析：可以通過 SQL 查詢、數據分析工具等輕鬆檢索和分析。

3. 常見形式：關係數據庫表格、電子表格（如 Excel）、CSV 文件等。

<br>

## 步驟

1. 使用 [yahoo! 財經](https://hk.finance.yahoo.com/quote/%5ETWII/history/) 資料取得數據。

2. 處理數據：將數據轉換為適合的格式，例如 `CSV` 或 `JSON` 格式。

3. 轉換為向量：使用合適的嵌入技術將數據轉換為向量表示。

4. 儲存向量：將轉換為向量的數據儲存在 `MongoDB Atlas` 中。

5. 查詢數據：使用向量搜索技術進行語義查詢。

6. `CSV 文件（Comma-Separated Values）` 儲存的是 `純文本格式` 中的 `結構化數據`，每行表示一個記錄，每個欄位之間用逗號分隔。 

<br>

## 開始實作

1. 收集數據：`台股大盤1997_2024.csv.csv`。

<br>

2. 先查看資料內容。

    ```python
    import pandas as pd
    import streamlit as st

    # 加載 CSV 文件
    def load_data(file_path):
        df = pd.read_csv(file_path)
        return df

    # Streamlit 介面
    st.title("檢查 CSV 文件結構和內容")

    # 加載數據
    file_path = "台股大盤1997_2024.csv"
    df = load_data(file_path)

    # 顯示列名和前幾行數據
    st.write("CSV 文件列名：")
    st.write(df.columns.tolist())

    st.write("CSV 文件前幾行數據：")
    st.write(df.head())
    ```

<br>

## 建立向量儲存和查詢應用

1. 這段代碼從一個名為 `taiwan_stock_data.csv` 的文件中加載台股數據，將其轉換為向量表示並儲存到MongoDB Atlas中，其中使用 `TfidfVectorizer` 將文本數據轉換為向量，並以 Streamlit 建立網頁進行用戶互動，允許用戶輸入問題並觸發查詢。

<br>

2. `taiwan_stock_data.csv` 文件應包含描述性文本數據（例如每日收盤評論或每年市場報告）以便進行向量化處理。

<br>

3. `delete_existing_data` 函數會刪除集合中的所有文件，確保在初始化新數據時不會超過空間配額，`perform_vector_search` 函數會根據輸入的查詢進行向量搜索，並返回最相似的前5個文件。

<br>

4. 完整程式碼。。

    ```python
    import os
    import pandas as pd
    import pymongo
    import pprint
    import certifi
    import json
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from pymongo import MongoClient
    from langchain_openai import ChatOpenAI
    import streamlit as st

    # 設置環境變數
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

    # 連接到 MongoDB Atlas
    client = MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
    db_name = "TaiwanStockDatabase"
    collection_name = "StockData"
    atlas_collection = client[db_name][collection_name]
    vector_search_index = "vector_index"

    # 刪除現有數據的函數
    def delete_existing_data():
        result = atlas_collection.delete_many({})
        return result.deleted_count

    # 載入 CSV 資料
    def load_data(file_path):
        df = pd.read_csv(file_path)
        return df

    # 建立向量儲存
    def initialize_data(file_path):
        # 刪除現有數據
        delete_existing_data()

        df = load_data(file_path)
        # 將每行數據拼接成一個描述字串
        df["description"] = df.apply(
            lambda row: f"日期: {row['Date']}, 開盤: {row['Open']}, 最高: {row['High']}, 最低: {row['Low']}, 收盤: {row['Close']}, 調整後收盤: {row['Adj Close']}, 成交量: {row['Volume']}",
            axis=1,
        )
        documents = df["description"].tolist()
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(documents)
        vectors_list = vectors.toarray().tolist()

        # 建立向量儲存
        for doc, vector in zip(documents, vectors_list):
            atlas_collection.insert_one({"description": doc, "embedding": vector})
        
        # 儲存向量化器詞彙表
        with open("tfidf_vocabulary.json", "w") as f:
            json.dump(vectorizer.vocabulary_, f)

    # 檢查集合是否為空，若為空則初始化資料
    if atlas_collection.count_documents({}) == 0 or not os.path.exists("tfidf_vocabulary.json"):
        print("初始化資料並創建向量儲存...")
        initialize_data("台股大盤2015_2024.csv")
    else:
        print("載入現有向量儲存...")

    # 執行向量搜索的函數
    def perform_vector_search(query, top_k=50):
        # 讀取向量化器詞彙表
        with open("tfidf_vocabulary.json", "r") as f:
            vocabulary = json.load(f)
        
        # 將查詢轉換為向量
        vectorizer = TfidfVectorizer(vocabulary=vocabulary)
        query_vector = vectorizer.fit_transform([query]).toarray()

        # 獲取所有已儲存的向量
        stored_vectors = list(
            atlas_collection.find({}, {"embedding": 1, "description": 1, "_id": 0})
        )
        descriptions = [v["description"] for v in stored_vectors]
        embeddings = [v["embedding"] for v in stored_vectors]

        # 計算餘弦相似度
        similarity_scores = cosine_similarity(query_vector, embeddings).flatten()
        sorted_indices = similarity_scores.argsort()[::-1]  # 按降序排列

        # 獲取前 top_k 個相似的文件
        top_documents = [descriptions[i] for i in sorted_indices[:top_k]]
        return top_documents

    # 使用OpenAI的模型來生成自然語言描述
    def generate_answer(question, top_documents):
        llm = ChatOpenAI()
        context = "\n".join(top_documents)
        prompt = f"根據以下台股歷史數據回答問題：\n\n{context}\n\n問題：{question}\n\n回答："
        response = llm.invoke(prompt)
        return response.content.strip()

    # 問題
    question = "請簡述台股在2024年全年度截至目前為止的市場表現"

    # 獲取相關文件
    top_documents = perform_vector_search(question)

    # 生成回答
    answer = generate_answer(question, top_documents)

    # 顯示結果
    print("回答：")
    print(answer)

    ```

<br>

5. 結果。

    ```bash
    載入現有向量儲存...
    回答：
    根據提供的數據，截至2024年5月24日，台股在2024年全年度的市場表現呈現穩定的趨勢。從開盤價、最高價、最低價、收盤價以及成交量等數據來看，台股整體呈現出波動較小、交易活躍的特徵。在此期間內，台股的收盤價呈現逐步上升的趨勢，表明投資者對於台股的信心增強，市場整體氛圍較為積極。然而，需要更多數據來進一步評估全年度的市場表現，以獲得更全面的分析結果。
    ```

<br>

6. 詢問其他問題 `請簡述台股在近五年的市場表現差異。`

    ```bash
    載入現有向量儲存...
    回答：
    根據提供的數據，我們可以看到在2018年2月至3月期間，台股的指數整體呈現下跌趨勢，並且波動幅度較大。而在2017年底至2018年初，台股指數則呈現較為穩定的表現。這顯示台股在近五年的市場表現存在較大的差異，且受到多個因素的影響，包括全球經濟環境、政治局勢、國際貿易關係等。投資者應該密切關注市場動態，制定合適的投資策略以應對市場波動。
    ```

<br>

___

_END_