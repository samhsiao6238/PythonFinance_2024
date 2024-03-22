# MongoDB

[官網](https://www.mongodb.com/zh-cn)

<br>

1. 點擊 `免費開始使用`。

    ![](images/img_69.png)

<br>

2. 使用 Google 帳號登入。

    ![](images/img_70.png)

<br>

3. 建立專案。

    ![](images/img_71.png)

<br>

4. 自訂專案名稱，然後點擊 `下一步`。

    ![](images/img_72.png)

<br>

5. 建立專案。
    
    ![](images/img_73.png)

<br>

6. 建立一個 `Cluster`。

    ![](images/img_74.png)

<br>

7. 選取 `免費`，其餘用預設值即可。

    ![](images/img_75.png)

<br>

8. 建立資料庫使用者。

    ![](images/img_76.png)

<br>

9. 選擇連線方法。

    ![](images/img_77.png)

<br>

10. 點擊後可查看連線指引。

    ![](images/img_78.png)

<br>

11. 使用指令安裝 Python 的 MogoDB 套件。

    ```bash
    python -m pip install pymongo
    ```

<br>

12. 開啟功能查可看腳本。

    ![](images/img_79.png)

<br>

13. 以下是複製下來的腳本，我另外加入一些說明，密碼部分 `<password>` 務必修改為自己的密碼，輸入時不要包含括號 `< >`，假如有自訂 `cluster` 名稱，也要修改 `appName` 之後的 `Cluster0`，範例如下。

    ```python
    # 導入庫
    from pymongo.mongo_client import MongoClient
    # 改為自己的密碼
    uri = "mongodb+srv://sam6238:sam112233@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # 建立連線實體
    client = MongoClient(uri)

    # 傳送連線請求
    try:
        client.admin.command('ping')
        print("成功連線到 MongoDB.")
    except Exception as e:
        print(e)
    ```

<br>

14. 在 `Jupyter NB` 中測試這個腳本，成功回傳表示連線成功。

    ![](images/img_80.png)

<br>

_以上連線 MongoDB 完成_

___

_END_