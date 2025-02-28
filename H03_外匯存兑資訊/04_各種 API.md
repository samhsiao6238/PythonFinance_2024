# 各種 API

<br>

## 敏感資訊

_使用 `.env` 儲存 API Key，並透過 `dotenv` 套件來讀取環境變數。_

<br>

1. 安裝 `python-dotenv`。

    ```bash
    pip install python-dotenv
    ```

<br>

2. 在專案目錄下建立 `.env` 與 `.gitignore` 檔案，並在 `.gitignore` 中寫入要忽略的檔案避免提交到 GitHub。

    ```bash
    touch .env .gitignore
    echo ".env" >> .gitignore
    ```

<br>

3. 在 `.env` 寫入以下內容。

    ```bash
    API_KEY=<填入自己的-API_KEY>
    ```

<br>

4. 更新 Python 代碼。

    ```python
    import os
    from dotenv import load_dotenv

    # 讀取 `.env` 檔案
    load_dotenv()

    # 取得 API Key
    API_KEY = os.getenv("API_KEY")
    ```

<br>

___

_未完_