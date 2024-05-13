import streamlit as st
from utility import get_neo4j_session, load_movie_data
# 載入 dotenv
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

    # 連接到資料庫
    session = get_neo4j_session(URI, USER, PASSWORD)

    # 載入數據
    movies = load_movie_data(session)

    # 顯示數據
    if movies:
        for movie in movies:
            st.write(f"Title: {movie['title']}, Released: {movie['released']}")
    else:
        st.write("No data found.")

    # 關閉資料庫對話
    session.close()


if __name__ == "__main__":
    main()
