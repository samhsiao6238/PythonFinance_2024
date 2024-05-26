# 向量儲存

_以處理圖片為例_

<br>

## 說明

1. 以下將進行一個典型的計算機視覺任務，處理圖片數據並將其轉換為向量嵌入並儲存在 MongoDB 中，將使用深度學習模型來完成最後的搜尋工作。

2. 至少需要10張圖片進行嵌入和查詢操作。圖片數量越多，向量儲存和查詢的效果會更好。

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
