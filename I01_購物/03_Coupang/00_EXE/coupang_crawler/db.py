import pymysql

def insert_into_db(data_list, db_config):
    connection = pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        charset='utf8mb4'
    )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coupang_products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    search_keyword VARCHAR(255),
                    title TEXT,
                    full_text TEXT,
                    price VARCHAR(50),
                    unit_price VARCHAR(50),
                    timestamp DATETIME
                );
            """)
            for data in data_list:
                cursor.execute("""
                    INSERT INTO coupang_products (search_keyword, title, full_text, price, unit_price, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    data["search_keyword"], data["title"], data["full_text"],
                    data["price"], data["unit_price"], data["timestamp"]
                ))
        connection.commit()
        print("✅ 已寫入資料庫。")
