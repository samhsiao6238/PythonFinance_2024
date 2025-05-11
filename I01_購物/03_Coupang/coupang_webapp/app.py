from flask import Flask, request, jsonify, render_template
import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import quote

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

    connection = pymysql.connect(**DB_CONFIG)
    seen_full_text = set()
    results = []

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT title, price, unit_price, full_text, timestamp FROM coupang_products ORDER BY timestamp DESC")
            for row in cursor.fetchall():
                full_text = row["full_text"]
                if all(kw in full_text for kw in keywords):
                    if full_text in seen_full_text:
                        continue
                    seen_full_text.add(full_text)
                    row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                    results.append(row)

    return jsonify(results)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json()
    keyword = data.get("keyword", "")
    advanced_keywords = data.get("advanced_keywords", [])

    if not keyword:
        return jsonify([])

    # 建立搜尋 URL
    encoded_keyword = quote(keyword)
    url = f"https://www.tw.coupang.com/search?q={encoded_keyword}&channel=user"

    # 啟動 Selenium
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=zh-TW")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    product_cards = soup.select("div.SearchResult_searchResultProduct___h6E9")
    now = datetime.now()
    display_results = []

    connection = pymysql.connect(**DB_CONFIG)
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
                )
            """)

            for card in product_cards:
                try:
                    full_text = card.get_text(separator=" ", strip=True)
                    title_tag = card.select_one("div.Product_title__8K0xk")
                    title = title_tag.get_text(strip=True) if title_tag else "N/A"
                    price_tag = card.select_one("span.Product_salePricePrice__2FbsL span")
                    price = price_tag.get_text(strip=True) if price_tag else "N/A"
                    unit_price_tag = card.select_one("div.Product_unitPrice__QQPdR")
                    unit_price = unit_price_tag.get_text(strip=True) if unit_price_tag else "N/A"

                    # ✅ 寫入資料庫（無條件寫入）
                    cursor.execute("""
                        INSERT INTO coupang_products (search_keyword, title, full_text, price, unit_price, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (keyword, title, full_text, price, unit_price, now))

                    # ✅ 只回傳符合進階條件的項目
                    if all(kw in full_text for kw in advanced_keywords):
                        display_results.append({
                            "title": title,
                            "price": price,
                            "unit_price": unit_price,
                            "full_text": full_text,
                            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
                        })

                except Exception as e:
                    print("⚠️ 寫入錯誤：", e)

            connection.commit()

    return jsonify(display_results)

if __name__ == "__main__":
    app.run(debug=True)
