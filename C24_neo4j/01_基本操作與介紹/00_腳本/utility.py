from neo4j import GraphDatabase


# 建立 Neo4j 資料庫驅動實例
def get_neo4j_driver(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


# 進行資料查詢
def load_movie_data(driver):
    with driver.session() as session:
        query = """
        MATCH (m:Movie)
        RETURN m.title AS title, m.released AS released LIMIT 10
        """
        result = session.run(query)
        movies = [
            {
                "title": record["title"],
                "released": record["released"]
            } for record in result
        ]
    return movies
