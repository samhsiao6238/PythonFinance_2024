# 導入庫
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

# 載入會員帳號密碼
EMAIL = os.getenv("COUPANG_EMAIL")
PASSWORD = os.getenv("COUPANG_PASSWORD")

# 關鍵字
search_keyword = "kose 洗面乳"
# 空列表會自動關閉篩選
advanced_keywords = ["2條"]

# 調用自訂「登入」模組，登入並取得 driver
driver = login_and_get_driver(EMAIL, PASSWORD)

# 調用自訂爬蟲模組，使用驅動器對關鍵字取回結果，並進行篩選
all_results, filtered_results = get_coupang_search_results(
    driver,
    search_keyword,
    advanced_keywords
)
driver.quit()

# 寫入資料庫，寫入所有取得的資料
if all_results:
    # 輸出資訊查看，在正式模式中可註解
    print("📦 寫入以下【所有搜尋結果】到資料庫：")
    for idx, r in enumerate(all_results, 1):
        print(f"{idx}. 標題: {r['title']}")
        print(f"   價格: {r['price']}")
        print(f"   單位價格: {r['unit_price']}")
        print(f"   時間戳: {r['timestamp']}")
        print("-" * 60)
    # 調用自訂模組寫入資料
    insert_into_db(all_results, db_config)
else:
    print("⚠️ 沒有搜尋結果，不進行資料庫寫入。")

# 在測試模式下可額外輸出進階結果查看
if advanced_keywords:
    print(
        f"\n🎯 符合條件（包含：{'、'.join(advanced_keywords)}）的結果："
    )
    # 假如有資料
    if filtered_results:
        for idx, r in enumerate(filtered_results, 1):
            print(f"{idx}. 標題: {r['title']}")
            print(f"   價格: {r['price']}")
            print(f"   單位價格: {r['unit_price']}")
            print(f"   時間戳: {r['timestamp']}")
            print("-" * 60)
    else:
        print("⚠️ 沒有符合進階條件的項目")