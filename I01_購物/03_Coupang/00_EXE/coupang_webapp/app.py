from flask import Flask, request, jsonify, render_template
import pymysql
import os
from dotenv import load_dotenv

# 載入 .env 設定
load_dotenv()

app = Flask(__name__)

# 資料庫連線參數
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    keywords = data.get("keywords", [])

    if not keywords:
        return jsonify([])

    # 建立資料庫連線
    connection = pymysql.connect(**DB_CONFIG)
    seen_full_text = set()
    results = []

    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT title, price, unit_price, full_text, timestamp FROM coupang_products ORDER BY timestamp DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

            for row in rows:
                full_text = row["full_text"]
                if all(kw in full_text for kw in keywords):
                    if full_text in seen_full_text:
                        continue
                    seen_full_text.add(full_text)
                    results.append(row)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)