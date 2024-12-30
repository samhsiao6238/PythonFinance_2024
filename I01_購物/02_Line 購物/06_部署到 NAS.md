# 部署到 NAS

_修改代碼，整合 NAS 中以 Docker 安裝的 Selenium 瀏覽器，並將數據儲存到 MariaDB 和 Excel_

<br>

## 準備工作

1. 連線 NAS。

    ```bash
    ssh sam6238@nas
    ```

<br>

2. 切換 root 使用權限。

    ```bash
    sudo -s
    ```

<br>

3. 進入專案目錄；這個資料夾在之前的專案已建立，假如不存在則先建立。

    ```bash
    cd /volume1/homes/sam6238/00_MyScript_2025
    ```

<br>

4. 加載虛擬環境。

    ```bash
    source ~/.profile
    ```

<br>

5. 安裝套件。

    ```bash
    pip install pymysql openpyxl tabulate
    ```

<br>

6. 建立腳本。

    ```bash
    touch exShoppingCoupon.py
    ```

<br>

7. 若需要處理敏感資訊，可使用既有的 `.env` 文件，透過指令查詢文件是否存在。

    ```bash
    ls -l  .env
    ```

<br>

## 代碼

_以下代碼也可在 `.ipynb` 中運行_

<br>

1. 以下代碼將使用 `webdriver.Remote` 連接到 Docker 中的 `selenium/hub`。

<br>

2. 並函數 `save_to_excel` 和 `save_to_mariadb`，分別儲存數據到本地 Excel 和 MariaDB。

<br>

3. 完整代碼。

    ```python
    import random
    import time
    import pandas as pd
    import pymysql
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # MariaDB 連線資訊
    db_config = {
        "host": "192.168.1.239",
        "port": 3306,
        "user": "sam6238",
        "password": "sam112233",
        "database": "testdb",
        "charset": "utf8mb4"
    }

    # Selenium Docker 端點
    SELENIUM_HUB_URL = "http://192.168.1.239:4444/wd/hub"

    # 配置 Selenium WebDriver
    def setup_webdriver():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        driver = webdriver.Remote(
            command_executor=SELENIUM_HUB_URL,
            options=options
        )
        return driver

    # 爬取數據
    def fetch_merchant_data(keywords):
        results = []
        driver = setup_webdriver()
        try:
            for keyword in keywords:
                URL = f"https://buy.line.me/s/{keyword}"
                driver.get(URL)
                # 隨機延遲
                time.sleep(random.uniform(2, 5))

                try:
                    # 查找商家名稱
                    merchant_name = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, 
                            "//div[@class='suggestedMerchantCards-title']/h2"
                        ))
                    ).text
                    # 查找回饋內容
                    cashback = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, 
                            "//div[@class='suggestedMerchantCards-point point']"
                        ))
                    ).text
                except Exception:
                    merchant_name = f"商店名稱 {keyword} 未找到"
                    cashback = "無"

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                results.append({
                    "商家名稱": merchant_name, 
                    "回饋": cashback, 
                    "查詢時間": timestamp
                })
        finally:
            driver.quit()

        return results

    # 儲存數據到 Excel
    def save_to_excel(data, file_name="merchant_data.xlsx"):
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)
        print(f"數據已儲存到本地 EXCEL 文件：{file_name}")

    # 儲存數據到 MariaDB
    def save_to_mariadb(data):
        connection = None
        cursor = None
        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            # 建立資料表
            create_table_query = """
            CREATE TABLE IF NOT EXISTS merchant_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                merchant_name VARCHAR(255) NOT NULL,
                cashback VARCHAR(50),
                query_time DATETIME
            );
            """
            cursor.execute(create_table_query)

            # 插入數據
            insert_query = """
            INSERT INTO merchant_data (merchant_name, cashback, query_time)
            VALUES (%s, %s, %s)
            """
            for item in data:
                cursor.execute(
                    insert_query, 
                    (
                        item["商家名稱"], 
                        item["回饋"], 
                        item["查詢時間"]
                    )
                )

            connection.commit()
            print("數據已成功寫入 MariaDB 資料庫。")
        except pymysql.MySQLError as e:
            print(f"寫入 MariaDB 資料庫失敗，錯誤：{e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # 主程序
    if __name__ == "__main__":
        keywords = [
            'Yahoo',
            '家樂福線上',
            '金車線上',
            'Apple',
            '蝦皮商城',
            '蝦皮超市',
            'adidas 官方',
            'NIKE',
            '寶雅',
            '松果',
            'PChome',
            'LG',
            '東森',
            '森森購物',
            '三立電電購'
        ]
        print("開始爬取數據...")
        data = fetch_merchant_data(keywords)
        print("爬取完成。")

        print("儲存數據到 EXCEL...")
        save_to_excel(data)

        print("儲存數據到 MariaDB...")
        save_to_mariadb(data)
        print("所有操作完成。")
    ```

<br>

## 讀取資料

1. 從資料庫讀取資料並存入 Excel。

    ```python
    from tabulate import tabulate

    output_excel_file = "data_from_db.xlsx"

    try:
        # 建立連線
        connection = pymysql.connect(**db_config)
        print("成功連線到 MariaDB。")

        # 建立游標
        cursor = connection.cursor()

        # 按商家名稱排序並獲取最新記錄
        query = """
        SELECT id, merchant_name, cashback, query_time
        FROM merchant_data
        ORDER BY merchant_name ASC, query_time DESC;
        """
        cursor.execute(query)

        # 獲取所有結果
        rows = cursor.fetchall()

        # 檢查是否有資料
        if rows:
            print("\nmerchant_data 表內容（按商家名稱排序）：")
            # 使用 tabulate 以表格方式顯示
            headers = ["ID", "商家名稱", "回饋", "查詢時間"]
            # 使用 "grid" 格式
            print(tabulate(rows, headers=headers, tablefmt="grid"))
            # 將結果轉換為 pandas DataFrame
            df = pd.DataFrame(rows, columns=headers)
            # 將 DataFrame 寫入 Excel
            df.to_excel(
                output_excel_file, 
                index=False, 
                engine='openpyxl'
            )
            print(f"\n數據已成功寫入到 Excel 文件：{output_excel_file}")
        else:
            print("merchant_data 表中無資料。")

    except pymysql.MySQLError as e:
        print(f"連線或查詢失敗，錯誤：{e}")

    except Exception as e:
        print(f"操作失敗，錯誤：{e}")

    finally:
        # 關閉連線
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    ```

<br>

___

_END_