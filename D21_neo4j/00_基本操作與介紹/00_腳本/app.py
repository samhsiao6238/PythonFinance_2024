import streamlit as st
from utility import get_neo4j_driver, load_movie_data
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 資料庫連接資訊
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


# Streamlit 主函數
def main():
    st.title("Neo4j Movie Data")

    # 創建驅動實例
    driver = get_neo4j_driver(URI, USER, PASSWORD)

    try:
        # 載入數據
        movies = load_movie_data(driver)

        # 顯示數據
        if movies:
            for movie in movies:
                st.write(
                    f"Title: {movie['title']}, Released: {movie['released']}"
                )
        else:
            st.write("No data found.")
    finally:
        # 確保無論如何都會關閉驅動器
        driver.close()


if __name__ == "__main__":
    main()
