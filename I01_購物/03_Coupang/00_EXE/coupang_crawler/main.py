import os
from dotenv import load_dotenv
from login import login_and_get_driver
from crawler import get_coupang_search_results
from db import insert_into_db

# 載入資料庫設定
load_dotenv()
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

search_keyword = "kose 洗面乳"
advanced_keywords = ["2條"]  # 可改為空清單以關閉篩選

# 登入與建立 driver
driver = login_and_get_driver()
print("✅ 已登入 Coupang")

# 取得全部與篩選結果
all_results, filtered_results = get_coupang_search_results(driver, search_keyword, advanced_keywords)
driver.quit()

# 寫入資料庫（全部資料）
if all_results:
    print("📦 寫入以下【所有搜尋結果】到資料庫：")
    for idx, r in enumerate(all_results, 1):
        print(f"{idx}. 標題: {r['title']}")
        print(f"   價格: {r['price']}")
        print(f"   單位價格: {r['unit_price']}")
        print(f"   時間戳: {r['timestamp']}")
        print("-" * 60)

    insert_into_db(all_results, db_config)
    print("✅ 已寫入資料庫。")
else:
    print("⚠️ 沒有搜尋結果，不進行資料庫寫入。")

# 額外輸出符合進階關鍵字的項目
if advanced_keywords:
    print(f"\n🎯 符合條件（包含：{'、'.join(advanced_keywords)}）的結果：")
    if filtered_results:
        for idx, r in enumerate(filtered_results, 1):
            print(f"{idx}. 標題: {r['title']}")
            print(f"   價格: {r['price']}")
            print(f"   單位價格: {r['unit_price']}")
            print(f"   時間戳: {r['timestamp']}")
            print("-" * 60)
    else:
        print("⚠️ 沒有符合進階條件的項目")
