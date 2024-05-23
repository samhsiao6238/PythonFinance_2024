# 新增一個 Tool

_尚未實測_

_在原本的專案中已有三個 Tool，這裡示範查詢 MongoDB。_

<br>

## 步驟

1. 首先，安裝 `pymongo` 庫。

    ```bash
    pip install pymongo
    ```

<br>

2. 接著，實作一個函數將自然語言查詢轉換為 MongoDB 查詢語句，這涉及使用一些簡單的規則或更多的自然語言處理技術來解析查詢。

    ```python
    import re
    from pymongo import MongoClient
    from typing import Any, Dict, List

    def parse_natural_language_query(nl_query: str) -> Dict[str, Any]:
        # 這是一個簡單的解析器範例，可以根據具體需求進行擴展
        query = {}
        if "name" in nl_query:
            match = re.search(r"name is (\w+)", nl_query)
            if match:
                query["name"] = match.group(1)
        return query

    def query_mongodb(nl_query: str, database_name: str, collection_name: str) -> List[Dict[str, Any]]:
        # 解析自然語言查詢
        query = parse_natural_language_query(nl_query)
        
        # 連接到 MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        
        # 選擇資料庫和集合
        db = client[database_name]
        collection = db[collection_name]
        
        # 執行查詢
        result = collection.find(query)
        
        # 將結果轉換為列表
        return list(result)
    ```

<br>

3. 最後，使用 `Tool.from_function` 將這個函數定義為工具並添加到 `tools` 列表中。

    ```python
    from langchain.tools import Tool

    tools = [
        # 添加
        Tool.from_function(
            name="MongoDB Query",
            description="用於查詢指定資料庫和集合的 MongoDB 查詢工具。",
            func=query_mongodb,
            return_direct=False,
        ),
        # 其餘工具 ...
        # ...
    ]
    ```

<br>

## 使用

1. 假設用戶提出以下問題。

    ```bash
    查詢名為 John Doe 的人的信息。
    ```

2. 模型應該生成以下步驟。

   - 識別用戶意圖是查詢 MongoDB
   - 將自然語言查詢轉換為 MongoDB 查詢語句
   - 調用 MongoDB Query 工具，並將結果返回給用戶

<br>

___

_END_