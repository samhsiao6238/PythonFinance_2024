# 向量儲存

_以處理圖片為例_

<br>

## 說明

1. 以下將進行一個典型的計算機視覺任務，處理圖片數據並將其轉換為向量嵌入並儲存在 MongoDB 中，將使用深度學習模型來完成最後的搜尋工作。

2. 至少需要10張圖片進行嵌入和查詢操作，圖片數量越多，向量儲存和查詢的效果會更好。

3. 文件採用以下結構進行儲存。

    ```bash
    project_directory/
    ├── image_folder/
    │   ├── image_1.jpg
    │   ├── image_2.jpg
    │   ├── image_3.jpg
    │   ├── ...
    │   └── image_10.jpg
    └── script.py  # 腳本存放於此
    ```

4. 初始化模型：這裡使用預訓練的 VGG16 模型，並去除最後一層，以獲取圖片的特徵嵌入。

5. 圖片嵌入函數：將圖片轉換為向量嵌入。

6. 儲存圖片嵌入：將圖片的嵌入儲存在 MongoDB 中。

7. 查詢圖片：計算查詢圖片與儲存圖片的相似度，並返回最相似的圖片。

<br>

## 前置作業

1. 先遍歷指定資料夾中的所有影像文件，包括 `.jpg`、`.jpeg`、`.png` 都轉換為相同的格式 `.jpg` 並儲存到同一資料夾中。

2. 安裝了 `Pillow` 庫。
```bash
pip install pillow
```
3. 程式碼。
```python
import os
from PIL import Image

def convert_images_to_jpg(source_folder, target_folder, output_format='jpg', target_size=(224, 224)):
    # 確保輸出格式是小寫
    output_format = output_format.lower()
    
    # 確保目標資料夾存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # 遍歷來源資料夾中的所有文件
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            source_file_path = os.path.join(source_folder, filename)
            img = Image.open(source_file_path)
            # 調整圖像大小
            img = img.resize(target_size, Image.ANTIALIAS)
            # 將文件名擷取出來
            base = os.path.splitext(filename)[0]
            # 新文件名
            new_filename = f"{base}.{output_format}"
            target_file_path = os.path.join(target_folder, new_filename)
            
            # 保存為指定格式到目標資料夾
            img.convert('RGB').save(target_file_path, output_format.upper())
            print(f"Converted {filename} to {new_filename} with size {target_size}")

# 指定來源資料夾和目標資料夾路徑
source_folder = "./source_images"  # 替換為你的來源資料夾路徑
target_folder = "./target_images"  # 替換為你的目標資料夾路徑

# 轉換所有圖片為 .jpg 格式，調整解析度並保存到目標資料夾
convert_images_to_jpg(source_folder, target_folder, output_format='jpg', target_size=(224, 224))

```

## 範例

1. 安裝所需的庫：

    - `tensorflow` 或 `torch`：用於加載和處理深度學習模型。
    - `pymongo`：用於連接和操作 MongoDB。
    - `numpy`：用於數據處理。
    - `sklearn.metrics.pairwise`：用於計算向量之間的相似度。

    ```bash
    pip install tensorflow pymongo numpy scikit-learn
    ```

<br>

2. 圖片向量化和儲存的步驟：

    ```python
    import os
    import numpy as np
    import pymongo
    import certifi
    from sklearn.metrics.pairwise import cosine_similarity
    from pymongo import MongoClient
    from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.models import Model
    import streamlit as st

    # 設置環境變數
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

    # 連接到 MongoDB Atlas
    client = MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
    db_name = "ImageDatabase"
    collection_name = "ImageData"
    atlas_collection = client[db_name][collection_name]

    # 初始化模型
    base_model = VGG16(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    # 定義圖片嵌入函數
    def get_image_embedding(img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        fc1_features = model.predict(img_data)
        return fc1_features.flatten()

    # 儲存圖片嵌入到 MongoDB
    def store_image_embeddings(image_folder):
        for img_name in os.listdir(image_folder):
            img_path = os.path.join(image_folder, img_name)
            embedding = get_image_embedding(img_path)
            atlas_collection.insert_one({"image_name": img_name, "embedding": embedding.tolist()})

    # 初始化資料
    image_folder = "./image_folder"  # 替換為圖片文件夾路徑
    store_image_embeddings(image_folder)

    # 執行向量搜索的函數
    def perform_vector_search(query_image_path):
        query_embedding = get_image_embedding(query_image_path)
        
        # 獲取所有已儲存的向量
        stored_vectors = list(atlas_collection.find({}, {"embedding": 1, "image_name": 1, "_id": 0}))
        image_names = [v["image_name"] for v in stored_vectors]
        embeddings = [v["embedding"] for v in stored_vectors]

        # 計算餘弦相似度
        similarity_scores = cosine_similarity([query_embedding], embeddings).flatten()
        sorted_indices = similarity_scores.argsort()[::-1]  # 按降序排列

        # 獲取最相似的圖片
        top_images = [image_names[i] for i in sorted_indices[:5]]
        return top_images

    # 查詢圖片
    query_image_path = "./image_folder/image_1.jpg"
    similar_images = perform_vector_search(query_image_path)

    # 顯示結果
    print("最相似的圖片：")
    for img in similar_images:
        print(img)
    ```

<br>

___

_END_
