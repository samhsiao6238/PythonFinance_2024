from neo4j import GraphDatabase


# 連接到 Neo4j 資料庫
def get_neo4j_session(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver.session()


# 載入電影數據
def load_movie_data(session):
    query = "MATCH (m:Movie) RETURN m.title AS title, m.released AS released LIMIT 10"
    result = session.run(query)
    movies = [
        {
            "title": record["title"],
            "released": record["released"]
        } for record in result
    ]
    return movies
