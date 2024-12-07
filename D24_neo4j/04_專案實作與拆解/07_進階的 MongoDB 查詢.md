# MongoDB 進階查詢

_使用 OpenAI 生成 MongoDB 查詢語法_

<br>

## 構想

1. 定義一個用於生成 MongoDB 查詢語法的模板：使用 PromptTemplate 來定義如何從自然語言問題生成 MongoDB 查詢語法。

<br>

2. 調用 OpenAI 模型生成查詢語法：使用 LangChain 來調用 OpenAI 模型並生成 MongoDB 查詢語法。

<br>

3. 執行生成的 MongoDB 查詢語法：使用 pymongo 執行生成的查詢語法並返回結果。

<br>

## 實作

1. 定義生成查詢語法的模板 `generate_mongo_advanced.py`。

    ```python
    # 定義 MongoDB 查詢語法生成模板
    MONGODB_QUERY_TEMPLATE = """
    你是一名專業的 MongoDB 開發者，將用戶的問題轉換為 MongoDB 查詢語句，以回答問題並提供資料。
    根據模式轉換用戶的問題。

    請務必使用以下集合和欄位名稱進行查詢：
    - 資料庫名稱: MyDatabase2024
    - 集合名稱: MyCollection2024
    - 欄位名稱: product_name (表示產品名稱)

    問題：
    {question}

    MongoDB 查詢語法：
    """

    # 使用模板建立一個 PromptTemplate 對象
    mongodb_prompt = PromptTemplate.from_template(MONGODB_QUERY_TEMPLATE)

    # 建立一個 LLMChain 對象，用於生成 MongoDB 查詢語法
    mongodb_chain = LLMChain(prompt=mongodb_prompt, llm=llm)
    ```

<br>

2. 繼續編輯 `generate_mongo_advanced.py` 腳本，添加函數來解析自然語言查詢，生成查詢語法並執行。

    ```python
    from pymongo import MongoClient
    import certifi
    from typing import Any, Dict, List
    import json
    import re

    def execute_mongodb_query(
        query: Dict[str, Any], database_name: str, collection_name: str, limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        執行 MongoDB 查詢
        :param query: 查詢條件
        :param database_name: 資料庫名稱
        :param collection_name: 集合名稱
        :param limit: 查詢結果的最大返回數量
        :return: 查詢結果列表
        """
        # 連接 MongoDB 資料庫
        URL = "mongodb+srv://sam6238:sam112233@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(
            URL, tlsCAFile=certifi.where(), tls=True, tlsAllowInvalidCertificates=True
        )
        db = client[database_name]
        collection = db[collection_name]

        try:
            # 執行查詢並限制返回數量
            result = collection.find(query).limit(limit)
            return list(result)
        except Exception as e:
            print(f"查詢時發生錯誤：{e}")
            return []


    def extract_query(text: str) -> str:
        """
        從生成的文本中提取 MongoDB 查詢語法
        :param text: 生成的文本
        :return: 查詢語法字串
        """
        match = re.search(r"find\((\{.*?\})\)", text)
        if match:
            return match.group(1)
        else:
            raise ValueError("未能從生成的文本中提取查詢語法")


    def validate_query_structure(query: str) -> str:
        """
        檢查並更改查詢語法中的集合名稱和欄位名稱
        :param query: 生成的查詢語法
        :return: 修正後的查詢語法
        """
        query = query.replace("db.collection.find", "db.MyCollection2024.find")
        query = query.replace("productName", "product_name")
        return query


    def mongodb_qa_advanced(nl_query: str) -> List[Dict[str, Any]]:
        """
        根據自然語言查詢生成 MongoDB 查詢語法並執行查詢
        :param nl_query: 自然語言查詢
        :return: 查詢結果列表
        """
        query_prompt = mongodb_chain.run({"question": nl_query})

        print(f"生成的查詢語法：{query_prompt}")

        try:
            # 提取查詢語法字串
            text = query_prompt.strip()

            # 驗證並修正查詢語法
            text = validate_query_structure(text)

            # 提取 MongoDB 查詢語法
            query_str = extract_query(text)
            print(f"提取的查詢語法：{query_str}")

            # 將查詢語法轉換為有效的 JSON 字串
            query_str = query_str.replace("'", '"')  # 更改單引號為雙引號
            query_str = re.sub(r"(\w+):", r'"\1":', query_str)  # 添加鍵的引號

            # 將查詢語法轉換為字典
            query = json.loads(query_str)

            # 確保查詢語法是字典
            if not isinstance(query, dict):
                raise ValueError("生成的查詢語法不是有效的字典格式")

            # 將產品名稱更改為中文
            if "product_name" in query and query["product_name"] == "Coca-Cola":
                query["product_name"] = "可口可樂"

            # 執行 MongoDB 查詢
            results = execute_mongodb_query(query, "MyDatabase2024", "MyCollection2024")
            if not results:
                print("查詢結果為空。")
            return results
        except ValueError as ve:
            print(f"提取查詢語法時發生錯誤：{ve}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤：{e}")
            return []
        except Exception as e:
            print(f"生成查詢語法時發生錯誤：{e}")
            return []
    ```

<br>

3. 導入到代理腳本 `agent.py` 中，新增工具，確保查詢順序，依序加入兩個 `MongoDB` 相關工具。

    ```python
    # 導入進階的 MongoDB 查詢函數
    from solutions.tools.generate_mongo_advanced import mongodb_qa_advanced

    # 工具
    tools = [
        # 處理一般聊天對話，涵蓋所有其他工具未涵蓋的問題和請求。
        Tool.from_function(
            name="General Chat",
            description="處理一般聊天對話，涵蓋所有其他工具未涵蓋的問題和請求。",
            func=llm.invoke,
            # 不要直接輸出
            return_direct=False,
        ),
        # 添加進階的 MongoDB 查詢工具
        Tool.from_function(
            name="Advanced MongoDB Query",
            description="用於生成和執行 MongoDB 查詢語法，適用於複雜的查詢需求。",
            func=mongodb_qa_advanced,
            return_direct=False
        ),
        # 添加 MongoDB 查詢
        Tool.from_function(
            name="Simple MongoDB Query",
            description="用於生成簡單的 MongoDB 查詢語法來回答問題。",
            func=mongodb_qa,
            return_direct=False
        ),
        # 用於基於向量搜索的電影情節訊息檢索。
        # 如果問題涉及搜尋與特定電影情節相似的電影，並且需要使用向量搜索技術，會使用此工具。
        Tool.from_function(
            name="Vector Search Index",
            description="用於基於向量搜索的電影情節訊息檢索。",
            func=kg_qa,
            # 不要直接輸出
            return_direct=False,
        ),
        # 用於使用 Cypher 查詢語句來回答有關電影的具體問題。
        # 如果問題需要從 Neo4j 資料庫中檢索電影訊息，並涉及生成和執行 Cypher 查詢。
        # 注意這裡會調用 cypher_qa
        Tool.from_function(
            # 這名稱會在終端機中顯示為 `Action：Cypher QA`
            name="Cypher QA",
            description="用於使用 Cypher 查詢語句來回答有關電影的具體問題。",
            # 調用 finetuned.py 中自訂的函數 cypher_qa
            func=cypher_qa,
            # 不可以直接回應，否則會出現解析錯誤
            return_direct=False,
        ),
    ]
    ```

<br>

4. 完整腳本：合併後的 `generate_mongo_advanced.py`。

    ```python
    from langchain.prompts.prompt import PromptTemplate
    from langchain.chains import LLMChain
    from solutions.llm import llm
    from pymongo import MongoClient
    import certifi
    from typing import Any, Dict, List
    import json
    import re

    # 定義 MongoDB 查詢語法生成模板
    MONGODB_QUERY_TEMPLATE = """
    你是一名專業的 MongoDB 開發者，將用戶的問題轉換為 MongoDB 查詢語句，以回答問題並提供資料。
    根據模式轉換用戶的問題。

    請務必使用以下集合和欄位名稱進行查詢：
    - 資料庫名稱: MyDatabase2024
    - 集合名稱: MyCollection2024
    - 欄位名稱: product_name (表示產品名稱)

    問題：
    {question}

    MongoDB 查詢語法：
    """

    # 使用模板建立一個 PromptTemplate 對象
    mongodb_prompt = PromptTemplate.from_template(MONGODB_QUERY_TEMPLATE)

    # 建立一個 LLMChain 對象，用於生成 MongoDB 查詢語法
    mongodb_chain = LLMChain(prompt=mongodb_prompt, llm=llm)


    def execute_mongodb_query(
        query: Dict[str, Any], database_name: str, collection_name: str, limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        執行 MongoDB 查詢
        :param query: 查詢條件
        :param database_name: 資料庫名稱
        :param collection_name: 集合名稱
        :param limit: 查詢結果的最大返回數量
        :return: 查詢結果列表
        """
        # 連接 MongoDB 資料庫
        URL = "mongodb+srv://sam6238:sam112233@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(
            URL, tlsCAFile=certifi.where(), tls=True, tlsAllowInvalidCertificates=True
        )
        db = client[database_name]
        collection = db[collection_name]

        try:
            # 執行查詢並限制返回數量
            result = collection.find(query).limit(limit)
            return list(result)
        except Exception as e:
            print(f"查詢時發生錯誤：{e}")
            return []


    def extract_query(text: str) -> str:
        """
        從生成的文本中提取 MongoDB 查詢語法
        :param text: 生成的文本
        :return: 查詢語法字串
        """
        match = re.search(r"find\((\{.*?\})\)", text)
        if match:
            return match.group(1)
        else:
            raise ValueError("未能從生成的文本中提取查詢語法")


    def validate_query_structure(query: str) -> str:
        """
        檢查並更改查詢語法中的集合名稱和欄位名稱
        :param query: 生成的查詢語法
        :return: 修正後的查詢語法
        """
        query = query.replace("db.collection.find", "db.MyCollection2024.find")
        query = query.replace("productName", "product_name")
        return query


    def mongodb_qa_advanced(nl_query: str) -> List[Dict[str, Any]]:
        """
        根據自然語言查詢生成 MongoDB 查詢語法並執行查詢
        :param nl_query: 自然語言查詢
        :return: 查詢結果列表
        """
        query_prompt = mongodb_chain.run({"question": nl_query})

        print(f"生成的查詢語法：{query_prompt}")

        try:
            # 提取查詢語法字串
            text = query_prompt.strip()

            # 驗證並修正查詢語法
            text = validate_query_structure(text)

            # 提取 MongoDB 查詢語法
            query_str = extract_query(text)
            print(f"提取的查詢語法：{query_str}")

            # 將查詢語法轉換為有效的 JSON 字串
            query_str = query_str.replace("'", '"')  # 更改單引號為雙引號
            query_str = re.sub(r"(\w+):", r'"\1":', query_str)  # 添加鍵的引號

            # 將查詢語法轉換為字典
            query = json.loads(query_str)

            # 確保查詢語法是字典
            if not isinstance(query, dict):
                raise ValueError("生成的查詢語法不是有效的字典格式")

            # 將產品名稱更改為中文
            if "product_name" in query and query["product_name"] == "Coca-Cola":
                query["product_name"] = "可口可樂"

            # 執行 MongoDB 查詢
            results = execute_mongodb_query(query, "MyDatabase2024", "MyCollection2024")
            if not results:
                print("查詢結果為空。")
            return results
        except ValueError as ve:
            print(f"提取查詢語法時發生錯誤：{ve}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤：{e}")
            return []
        except Exception as e:
            print(f"生成查詢語法時發生錯誤：{e}")
            return []

    ```

<br>

## 警告

1. 出現以下警告訊息，但運作是正常的。

    ```bash
    /Users/samhsiao/Documents/PythonVenv/env0521/lib/python3.11/site-packages/langchain_core/_api/deprecation.py:119: LangChainDeprecationWarning: The class `LLMChain` was deprecated in LangChain 0.1.17 and will be removed in 0.3.0. Use RunnableSequence, e.g., `prompt | llm` instead.
    warn_deprecated(
    ```

<br>

___

_這個範例暫且到這，接下來我想嘗試透過 MongoDB 官方與 LangChain 整合文件進行優化。_
