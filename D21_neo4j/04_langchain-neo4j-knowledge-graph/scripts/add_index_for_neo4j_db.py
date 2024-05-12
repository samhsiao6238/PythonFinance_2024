'''
執行這個腳本的目的是在 Neo4j 資料庫中建立兩種索引：文字索引和全文索引。
'''
# 引入os模組，用於作業系統功能，如環境變量
import os
# 從neo4j模組引入GraphDatabase，用於連接和操作Neo4j資料庫
from neo4j import GraphDatabase
# 從dotenv模組引入load_dotenv，用於載入.env檔案中的環境變量
from dotenv import load_dotenv
# 從.env檔案載入環境變量
load_dotenv()


# 主函數定義
def main():
    # 建立Neo4j資料庫的連接
    driver = GraphDatabase.driver(
        # 從環境變數取得資料庫的連線URI
        uri=os.getenv("NEO4J_DB_URI"),
        # 使用環境變數中的使用者名稱和密碼進行認證
        auth=(
            os.getenv("NEO4J_DB_USER"),
            os.getenv("NEO4J_DB_PASS"),
        ),
        # 指定要連接的資料庫名稱
        database=os.getenv("NEO4J_DB_NAME"),
    )

    # 使用with語句管理資料庫會話，確保會話最終能正確關閉
    with driver.session() as session:
        # 執行Cypher指令建立文字索引，如果索引不存在則建立
        session.run(
            "CREATE TEXT INDEX idx_node_entity_name IF NOT EXISTS FOR (n:Entity) ON (n.name)"
        )
        # 執行Cypher指令建立全文索引，指定分詞器為中日韓（CJK）
        session.run(
            f"CREATE FULLTEXT INDEX {os.getenv('NEO4J_ENTITY_NAME_FULLTEXT_INDEX_NAME')} IF NOT EXISTS "
            + "FOR (n:Entity) "
            + "ON EACH [n.name] "
            + "OPTIONS {indexConfig: {`fulltext.analyzer`: 'cjk'}}"
        )


# 當腳本直接執行時執行以下程式碼
if __name__ == "__main__":
    try:
        # 呼叫main函數
        main()
    # 捕捉鍵盤中斷異常（如使用者按Ctrl+C）
    except KeyboardInterrupt:
        # 列印中斷訊息
        print("Keyboard interrupt, quitting")
