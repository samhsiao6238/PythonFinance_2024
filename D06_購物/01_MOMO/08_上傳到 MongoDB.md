# 上傳到 MongoDB

_讀取 Firebase 節點上的資料，然後寫入 MongoDB_

<br>

## 腳本說明

1. 以下要自定義一個資料庫（Database）名稱、一個集合（Collection）名稱。

<br>

2. 完整腳本。

```python
# 導入庫
from pymongo.mongo_client import MongoClient
import firebase_admin
from firebase_admin import credentials, db

# Firebase初始化
cred = credentials.Certificate('fir-2024-6e360-firebase-adminsdk-16wwf-d2983e1f68.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-2024-6e360-default-rtdb.firebaseio.com/'
})

# MongoDB 連接設定
uri = "mongodb+srv://sam6238:sam112233@cluster0.yhwvqqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# 建立 MongoDB 數據庫和集合
mongodb = client['MyDatabase2024']
collection = mongodb['MyCollection2024']

# 從Firebase讀取數據
ref = db.reference('momo')
momo_data = ref.get()

# 檢查是否成功獲取數據
if momo_data:
    print("成功從Firebase讀取數據.")
    # 將數據存儲到MongoDB
    try:
        result = collection.insert_many([{'product_name': key, **value} for key, value in momo_data.items()])
        print(f"成功將資料儲存到MongoDB, 插入的文檔ID: {result.inserted_ids}")
    except Exception as e:
        print(f"將數據存儲到MongoDB時發生錯誤: {e}")
else:
    print("從Firebase讀取數據失敗或數據為空.")

# 關閉MongoDB連接
client.close()
```

<br>