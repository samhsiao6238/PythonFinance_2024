# Cypher

<br>

## 簡介

1. Cypher 是 Neo4j 圖形資料庫管理系統的查詢語言，專為便利地查詢、更新和管理圖表資料而設計。

2. Cypher 的語法與 SQL 類似，但專門針對圖形結構的操作進行了最佳化，允許使用者以聲明式方式描述需要的圖形模式，而不是編寫底層程式碼來實現資料存取和操作。

<br>

## Cypher 與 Neo4j 的關係

1. Cypher 是 Neo4j 的本地查詢語言，這表示它是為了最大化 Neo4j 圖形資料庫的效能而專門開發的。

2. 使用 Cypher 可以透過簡單的聲明式語句直觀地表示複雜的圖形查詢和資料關係，例如尋找兩個節點之間的最短路徑、執行深度搜尋、或是匹配複雜的圖形模式。

<br>

## Cypher 與 Python 的關係

1. Python 透過多種函式庫與 Neo4j 資料庫互動，其中最主要的是官方的 Neo4j Python 驅動程式，這個驅動程式允許 Python 開發者在應用程式中執行 Cypher 查詢語句、連接到 Neo4j 實例，並對圖資料執行 CRUD（建立、讀取、更新、刪除）操作。

2. 使用 Python 和 Neo4j 的組合可利用 Python 的簡潔語法和強大的資料處理能力以及 Neo4j 的高效圖資料管理能力，來建立複雜的資料分析、機器學習和網路服務應用程式。

<br>

## 範例

1. 在以下範例中，Python 腳本透過 Cypher 查詢來找出名為 Alice 的人的所有朋友，並印出他們的名字。

<br>

2. Cypher 查詢。

    ```python
    from neo4j import GraphDatabase

    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "your_password"

    driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_friends_of(name):
        with driver.session() as session:
            result = session.run("MATCH (p:Person)-[:FRIENDS_WITH]->(friend) WHERE p.name = $name RETURN friend.name", name=name)
            for record in result:
                print(record["friend.name"])

    get_friends_of("Alice")
    ```


<br>

___

_END_