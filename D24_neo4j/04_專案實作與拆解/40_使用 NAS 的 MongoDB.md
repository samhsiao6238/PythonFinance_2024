# 連線

_已經在 NAS 上架設好_

## 說明

1. 接下來的操作是透過 Python 腳本連接到 NAS 上的 MongoDB 容器。

<br>

2. 此腳本將使用 `pymongo` 庫。

    ```bash
    pip install pymongo
    ```

<br>

3. 完整範例。

    ```python
    # 導入 MongoClient 類來進行 MongoDB 連接
    from pymongo import MongoClient

    # 設置 MongoDB 連接 URI，包含帳號、密碼和 NAS 的 IP 地址及端口
    MONGODB_URI = "mongodb://sam6238:sam112233@192.168.1.240:21017/"

    # 使用 MongoClient 類進行連接
    client = MongoClient(MONGODB_URI)

    # 測試基本連接
    try:
        # 使用 admin 資料庫的命令來測試連接
        db = client.admin.command('ping')
        print("MongoDB 連接成功:", db)
    except Exception as e:
        # 如果連接失敗，捕獲並打印異常信息
        print("MongoDB 連接失敗:", e)
    ```

<br>

## 說明

1. 導入 `MongoClient` 類：

    ```python
    from pymongo import MongoClient
    ```

<br>

2. 設置 MongoDB 連接 URI。

    ```python
    MONGODB_URI = "mongodb://sam6238:sam112233@192.168.1.240:5000/"
    ```

<br>

3. 使用 `MongoClient` 進行連接：

    ```python
    # 創建了一個 `MongoClient` 對象
    client = MongoClient(MONGODB_URI)
    ```

<br>

4. 測試基本連接：

    ```python
    try:
        # 使用 `admin` 資料庫的 `ping` 命令來測試連接
        db = client.admin.command('ping')
        print("MongoDB 連接成功:", db)
    except Exception as e:
        print("MongoDB 連接失敗:", e)
    ```

<br>

___

_END_