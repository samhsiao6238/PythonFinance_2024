# 從 MongoDB 讀取資料

<br>

## 關於文件查詢

_以下說明如何查詢文件_

<br>

1. 在瀏覽器中搜尋 `mongodb`，點擊進入[文件](https://www.mongodb.com/docs/)。

    ![](images/img_97.png)

<br>

2. 或是在官網內選取 `文件`。
    
    ![](images/img_98.png)

<br>

3. 點擊放大鏡搜尋。

    ![](images/img_99.png)

<br>

4. 查詢 `MongoDB API Reference`。
    
    ![](images/img_100.png)

<br>

5. 結構上來說，位置在。
    
    ![](images/img_101.png)

<br>

6. 從右側導覽中可以看到相關函數。

    ![](images/img_102.png)

<br>

7. 點擊後便可以查看詳細的語法說明與範例。

    ![](images/img_103.png)

<br>

## 腳本

<br>

1. 完整腳本。

    ```python
    # 導入庫
    from pymongo.mongo_client import MongoClient

    # MongoDB 連接設定
    uri = "mongodb+srv://<輸入自己的帳號>:<輸入自己的密碼>@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri)

    # 建立 MongoDB 數據庫和集合
    mongodb = client['MyDatabase2024']
    collection = mongodb['MyCollection2024']

    # 從 MongoDB 讀取數據
    try:
        documents = collection.find({})
        for document in documents:
            print(document)
        print("成功從MongoDB讀取數據.")
    except Exception as e:
        print(f"從MongoDB讀取數據時發生錯誤: {e}")

    # 關閉 MongoDB 連接
    client.close()
    ```

<br>

2. 會顯示如下結果。

    ![](images/img_85.png)

<br>

___


_END_