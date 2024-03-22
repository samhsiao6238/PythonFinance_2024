# 從 MongoDB 讀取資料

<br>

## 腳本

1. 完整腳本。

    ```python
    # 導入庫
    from pymongo.mongo_client import MongoClient

    # MongoDB 連接設定
    uri = "mongodb+srv://sam6238:sam112233@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
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