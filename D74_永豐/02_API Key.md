# API Key

_登入 [官網](https://www.sinotrade.com.tw/newweb/)_

<br>

## 管理 API Key

1. 登入官網後，展開功能，選取 `API 管理`。

    ![](images/img_27.png)

<br>

2. 新增 API Key。

    ![](images/img_28.png)

<br>

3. 先進行相關驗證。

    ![](images/img_29.png)

<br>

4. 建立新的 API Key。

    ![](images/img_01.png)

<br>

5. 完成後複製密鑰並且下載憑證。

    ![](images/img_02.png)

<br>

## 編輯敏感資訊

1. 在專案根目錄添加文件 `.env`，並編輯既有文件 `.gitignore`，寫入 `.env` 避免將敏感資訊上傳。

    ```json
    touch .env
    ```

<br>

2. 編輯 `.env` 文件，貼上以下內容；其中 `CA_PASSWORD` 就是用戶的身分證字號，第一碼大寫；如有必要可參考 [官網影片](https://www.youtube.com/watch?v=0tPCZiRsz-U&t=84s)。

    ```bash
    API_KEY=<輸入-API_Key>
    SECRET_KEY=<輸入-Secret_Key>
    CA_CERT_PATH=Sinopac.pfx
    CA_PASSWORD=<輸入用戶密碼>
    ```

<br>

## 編輯腳本

1. 導入套件。

    ```python
    import os
    from dotenv import load_dotenv
    ```

<br>

2. 載入環境變數。

    ```python
    load_dotenv()
    ```

<br>

3. 編輯既有的 `main()` 函數，覆蓋原本內容即可。

    ```python
    def main():
        api = sj.Shioaji(simulation=True)
        api.login(
            api_key=os.environ["API_KEY"],
            secret_key=os.environ["SECRET_KEY"],
            fetch_contract=False
        )
        api.activate_ca(
            ca_path=os.environ["CA_CERT_PATH"],
            ca_passwd=os.environ["CA_PASSWORD"],
        )
        print("login and activate ca success")
    ```

<br>

4. 編輯 `pyproject.toml`，在 `[project.scripts]` 區塊加入指令。

    ```toml
    [project.scripts]
    main = "sj_trading:main"
    hello = "sj_trading:hello"
    ```

<br>

5. 測試登入。

    ```bash
    uv run main
    ```

    ![](images/img_12.png)

<br>

___

_END_