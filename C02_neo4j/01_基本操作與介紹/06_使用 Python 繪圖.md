# 繪圖

_使用 Cypher 語法讀取資料庫後進行繪圖_

<br>

## 步驟

1. 安裝套件：這個範例將使用 `networkx` 作為與 `Matplotlib` 的接口來進行繪圖。

    ```python
    pip install networkx
    ```

<br>

2. 程式碼：使用腳本進行繪製。

    ```python
    from neo4j import GraphDatabase
    import networkx as nx
    import matplotlib.pyplot as plt
    import os
    from dotenv import load_dotenv

    # 環境變數
    load_dotenv()

    # 使用自己的資料庫連接
    YOUR_URI = os.getenv("NEO4J_URI")
    YOUR_USER = os.getenv("NEO4J_USERNAME")
    YOUR_PASSWORD = os.getenv("NEO4J_PASSWORD")

    # 建立 Neo4j 連線
    driver = GraphDatabase.driver(YOUR_URI, auth=(YOUR_USER, YOUR_PASSWORD))


    def fetch_data():
        # 可更改這段語法來繪製不同的圖
        # 或是將這個部分改為參數傳入
        """從 Neo4j 中提取數據"""
        query = """
        MATCH p=()-[:ACTED_IN]->() RETURN p LIMIT 25;
        """
        data = []
        with driver.session() as session:
            results = session.run(query)
            for record in results:
                for rel in record["p"].relationships:
                    data.append({
                        "start_node": rel.start_node,
                        "end_node": rel.end_node,
                        "type": rel.type,
                        "properties": dict(rel)
                    })
        return data

    # 從 Neo4j 中提取數據
    data = fetch_data()

    # 建立 NetworkX 圖形
    G = nx.Graph()

    for item in data:
        start, end = item["start_node"], item["end_node"]
        G.add_node(start.id, label=start["name"] if "name" in start.keys() else "Unnamed")
        G.add_node(end.id, label=end["name"] if "name" in end.keys() else "Unnamed")
        G.add_edge(start.id, end.id, type=item["type"])

    '''繪圖'''
    # 定義佈局
    pos = nx.spring_layout(G)
    labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    nx.draw(G, pos, labels=labels, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G[u][v]['type'] for u, v in G.edges()})
    plt.show()

    # 關閉驅動器
    driver.close()
    ```

<br>

3. 成果圖。

    ![](images/img_37.png)

<br>

## 關於腳本中的 Cypher 語法

1. 語法可以透過點擊面板來取得。

    ```bash
    MATCH p=()-[:DIRECTED]->() RETURN p LIMIT 25;
    ```

    ![](images/img_42.png)

<br>

2. 相同的語法在面板上的繪製還是漂亮一點，這裡主要是提供另一種選項。

    ![](images/img_43.png)

<br>

___

_END_