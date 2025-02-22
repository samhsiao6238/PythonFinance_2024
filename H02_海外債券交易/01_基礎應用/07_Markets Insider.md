# Markets Insider

_Markets Insider 是 Business Insider 旗下的財經資訊平台，專門提供即時金融市場數據、股票報價、外匯、加密貨幣、期貨、商品價格等投資相關資訊。_

<br>

![](images/img_23.png)

<br>

## 說明

_以下嘗試從 `Markets Insider` 網站取得標的商品的歷史交易紀錄，這裡以 `US02209SBE28` 為例。_

<br>

## 搜尋所需的封包

1. 訪問 [Markets Insider](https://markets.businessinsider.com/) 網站。

<br>

2. 在右上方輸入 ISIN Code `US02209SBE28` 進行搜尋。

    ![](images/img_24.png)

<br>

3. 下方會顯示圖表，以下就是要來取得這張圖表中的歷史紀錄。

    ![](images/img_25.png)

<br>

## 開始操作

1. 在瀏覽器點擊 `F12` 進行檢視。

<br>

2. 點擊 `Network` 然後切換到 `Fetch/XHR`。

    ![](images/img_26.png)

<br>

3. 在 `Name` 欄位內任意選取一個項目，然後右邊切換到 `Respopnse`。

    ![](images/img_27.png)

<br>

4. 在這個步驟需要逐一人工檢查，然後會在 `Chart...` 的項目下看到所需的歷史交易紀錄，也是網頁中用來繪製圖表的數據。

    ![](images/img_28.png)

<br>

5. 也可以直接點擊。

    ![](images/img_29.png)

<br>

6. 會在瀏覽器中展開這個資料。

    ![](images/img_30.png)

<br>

7. 可以點擊 `Preview` 來展開資料查看，至此已經找到所需的封包。

    ![](images/img_31.png)

<br>

8. 切換到 `Headers`，在 `Request URL` 的部分，使用的方法是 `GET`，這些都是重要的資訊，後面都還會用到。

    ![](images/img_32.png)

<br>

## 解析

1. 取得全部資訊。

    ```python
    import requests
    import json
    import time

    # API URL
    url = "https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Bond&tkData=1,46441575,1330,333&from=19700201&to=20250219"

    # 加入 `User-Agent` 模擬瀏覽器
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 重試機制
    max_attempts = 3
    attempt = 0
    # 儲存 API 回應的數據
    data = None

    while attempt < max_attempts:
        try:
            print(
                "🔍 正在查詢債券數據"
                f" (嘗試 {attempt + 1}/{max_attempts}) ..."
            )
            response = requests.get(
                url, headers=headers, timeout=15
            )
            
            # 檢查回應是否成功
            if response.status_code == 200:
                print("✅ API 請求成功，完整回應內容如下：")
                # 完整輸出 API 回應
                print(response.text)
                # 直接跳出迴圈
                break
            else:
                print(
                    f"❌ 請求失敗，狀態碼: {response.status_code}"
                )
        
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(
                f"⚠️ 查詢超時，正在重試 ({attempt+1}/{max_attempts}) ..."
            )

        attempt += 1
        # 等待 5 秒後重試
        time.sleep(5)
    ```

<br>

2. 篩選交易資訊；`instrumentType=Bond` 指定查詢的是 `債券`，`tkData=1,46441575,1330,333` 用於特定債券的標識符，不同債券會有不同的 `tkData`，`from=19700201&to=20231216` 指定查詢時間範圍。

    ```python
    import requests
    import json
    import pandas as pd

    # API URL
    url = "https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Bond&tkData=1,46441575,1330,333&from=19700201&to=20250219"

    # 加入 `User-Agent` 模擬瀏覽器
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 發送請求
    response = requests.get(url, headers=headers, timeout=15)

    # 解析回應數據
    if response.status_code == 200:
        data = json.loads(response.text)

        # 轉換為 DataFrame
        df = pd.DataFrame(data)

        # 確保日期欄位是遞增排序
        df['Date'] = pd.to_datetime(df['Date'])
        # 按日期降序排序，最新的排在最前面
        df = df.sort_values(by='Date', ascending=False)

        # 提取最新交易日的數據
        # 最新一筆交易數據
        latest_trade = df.iloc[0]

        # 顯示結果
        latest_info = {
            "日期": latest_trade["Date"].strftime('%Y-%m-%d'),
            "收盤價": latest_trade["Close"],
            "開盤價": latest_trade["Open"],
            "最高價": latest_trade["High"],
            "最低價": latest_trade["Low"],
            "交易量": latest_trade["Volume"]
        }

        print("📊 最新債券交易資訊：")
        for key, value in latest_info.items():
            print(f"{key}: {value}")

    else:
        print(f"❌ API 查詢失敗，狀態碼: {response.status_code}")
    ```

    ![](images/img_33.png)

<br>

## 儲存標資訊

1. 查詢並儲存指定標的資訊。

    ```python
    import requests
    import pandas as pd
    from datetime import datetime

    # URL 從哪裡取得資料
    url = "https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Bond&tkData=1,46441575,1330,333&from=19700201&to=20250220"

    # 發送請求取得資料
    response = requests.get(url)

    # 檢查響應狀態碼，確保請求成功
    if response.status_code == 200:
        # 解析 JSON 數據
        data = response.json()

        # 轉換為 DataFrame
        df = pd.DataFrame(data)

        # 將日期從字串轉換為 datetime 對象
        df['Date'] = pd.to_datetime(df['Date'])

        # 儲存為 Excel 文件
        excel_file = 'data/MarketsInsider_數據.xlsx'
        df.to_excel(
            excel_file, index=False
        )

        print(f"數據已儲存到 {excel_file}")
    else:
        print(
            "Failed to retrieve data:",
            response.status_code
        )
    ```

<br>

## 對照

1. 這是對照表，提供做為參考，後續可作為獨立文件繼續拓展，無需寫入每一個腳本中。

    ```python
    isin_to_name = {
        'US02209SBF92': '高特力 2039 5.95', "1,46441569,1330,333",
        'US037833BX70': '蘋果 2046 4.65', "1,31618402,1330,333",
        'US02209SBE28': '高特力 2039 5.8', "1,46441575,1330,333",
        'US716973AH54': '輝瑞 2053 5.3', "1,127132136,1330,333",
        'US842434DA71': '南加州天然氣 2054 5.6', "",
        'US872898AJ06': '台積電 2052 4.5', "1,118393079,16,333",
        'USF2893TAE67': '法國電力 2040 5.6', "1,10955366,1330,333",
        'US05526DBV64': '英美菸草 2052 4.65', "1,117582253,1330,333",
        'US717081ED10': '輝瑞 2046 4.125', "",
        'US716973AG71': '輝瑞 2053 5.3', "1,127131476,1330,333",
    }
    ```

<br>

2. 批次查詢。

    ```python
    import requests
    import pandas as pd
    from datetime import datetime

    # ISIN 對應的 tkData
    isin_to_tkdata = {
        'US02209SBF92': ('高特力 2039 5.95', '1,46441569,1330,333'),
        'US037833BX70': ('蘋果 2046 4.65', '1,31618402,1330,333'),
        'US02209SBE28': ('高特力 2039 5.8', '1,46441575,1330,333'),
        'US716973AH54': ('輝瑞 2053 5.3', '1,127132136,1330,333'),
        'US842434DA71': ('南加州天然氣 2054 5.6', ''),  # 尚未查到
        'US872898AJ06': ('台積電 2052 4.5', '1,118393079,16,333'),
        'USF2893TAE67': ('法國電力 2040 5.6', '1,10955366,1330,333'),
        'US05526DBV64': ('英美菸草 2052 4.65', '1,117582253,1330,333'),
        'US717081ED10': ('輝瑞 2046 4.125', ''),  # 尚未查到
        'US716973AG71': ('輝瑞 2053 5.3', '1,127131476,1330,333')
    }

    # 查詢時間範圍
    start_date = "19700201"
    end_date = "20250220"

    # 儲存所有數據的 DataFrame 字典
    all_data = {}

    # 遍歷每個 ISIN，查詢價格數據
    for isin, (bond_name, tk_data) in isin_to_tkdata.items():
        print(f"\n🔍 正在查詢 {bond_name} ({isin}) ...")

        if not tk_data:
            print(f"⚠️ 無法取得 {bond_name} ({isin}) 的 tkData，跳過")
            # 若無 tkData，直接跳過
            continue

        # 設定 API URL
        url = f"https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Bond&tkData={tk_data}&from={start_date}&to={end_date}"
        
        # 發送請求
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                # 若 API 回傳空數據，則跳過
                if not data:
                    print(f"⚠️ {bond_name} ({isin}) 無數據，跳過")
                    continue

                # 轉換為 DataFrame
                df = pd.DataFrame(data)
                # 日期格式 yyyy/mm/dd
                df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y/%m/%d')

                # 只保留 Close 欄位
                df = df[['Date', 'Close']]

                # 加入 ISIN 和 Bond Name
                df.insert(1, 'ISIN', isin)
                df.insert(2, 'Bond Name', bond_name)

                # 加入至數據字典
                all_data[bond_name] = df
                print(
                    f"✅ {bond_name} ({isin}) 數據取得成功，"
                    f"共 {len(df)} 筆"
                )

            except Exception as e:
                print(
                    f"❌ 解析 {bond_name} ({isin}) "
                    f"JSON 失敗: {e}"
                )
        else:
            print(
                f"❌ {bond_name} ({isin}) 查詢失敗，"
                f"HTTP 狀態碼: {response.status_code}"
            )

    # 儲存至 Excel，每支債券分開存放在不同的 Sheet
    if all_data:
        excel_file = 'data/MI_歷史數據_全.xlsx'
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            for sheet_name, df in all_data.items():
                # Excel Sheet 名稱最多 31 字元
                sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(
            f"\n📊 所有數據已儲存至 {excel_file}，"
            "每支債券單獨存放在不同的 Sheet"
        )
    else:
        print("\n⚠️ 無有效數據，未儲存 Excel 檔案")
    ```

<br>

2. 若要儲存個別文件。

    ```python
    import requests
    import pandas as pd
    from datetime import datetime

    # ISIN 對應的 tkData
    isin_to_tkdata = {
        'US02209SBF92': ('高特力 2039 5.95', '1,46441569,1330,333'),
        'US037833BX70': ('蘋果 2046 4.65', '1,31618402,1330,333'),
        'US02209SBE28': ('高特力 2039 5.8', '1,46441575,1330,333'),
        'US716973AH54': ('輝瑞 2053 5.3', '1,127132136,1330,333'),
        'US842434DA71': ('南加州天然氣 2054 5.6', ''),  # 尚未查到
        'US872898AJ06': ('台積電 2052 4.5', '1,118393079,16,333'),
        'USF2893TAE67': ('法國電力 2040 5.6', '1,10955366,1330,333'),
        'US05526DBV64': ('英美菸草 2052 4.65', '1,117582253,1330,333'),
        'US717081ED10': ('輝瑞 2046 4.125', ''),  # 尚未查到
        'US716973AG71': ('輝瑞 2053 5.3', '1,127131476,1330,333')
    }

    # 查詢時間範圍
    start_date = "19700201"
    end_date = "20250220"

    # 遍歷每個 ISIN，查詢價格數據
    for isin, (bond_name, tk_data) in isin_to_tkdata.items():
        print(f"\n🔍 正在查詢 {bond_name} ({isin}) ...")

        if not tk_data:
            print(f"⚠️ 無法取得 {bond_name} ({isin}) 的 tkData，跳過")
            # 若無 tkData，直接跳過
            continue

        # 設定 API URL
        url = f"https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Bond&tkData={tk_data}&from={start_date}&to={end_date}"
        
        # 發送請求
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                # 若 API 回傳空數據，則跳過
                if not data:
                    print(f"⚠️ {bond_name} ({isin}) 無數據，跳過")
                    continue

                # 轉換為 DataFrame
                df = pd.DataFrame(data)
                # 日期格式 yyyy/mm/dd
                df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y/%m/%d')

                # 只保留 Close 欄位
                df = df[['Date', 'Close']]

                # 加入 ISIN 和 Bond Name
                df.insert(1, 'ISIN', isin)
                df.insert(2, 'Bond Name', bond_name)

                # 設定儲存的 Excel 檔名
                excel_filename = f"data/MI_歷史數據_{isin}_{start_date}-{end_date}.xlsx"

                # 儲存為獨立的 Excel 文件
                df.to_excel(excel_filename, index=False)
                print(
                    f"✅ {bond_name} ({isin}) "
                    f"數據儲存至 {excel_filename}"
                )

            except Exception as e:
                print(f"❌ 解析 {bond_name} ({isin}) JSON 失敗: {e}")
        else:
            print(
                f"❌ {bond_name} ({isin}) 查詢失敗，"
                f"HTTP 狀態碼: {response.status_code}"
            )

    print("\n📊 所有數據下載完成！")
    ```

<br>

___

_未完_