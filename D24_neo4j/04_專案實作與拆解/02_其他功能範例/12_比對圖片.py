import os
import certifi
from pymongo import MongoClient
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ssl
import matplotlib.pyplot as plt
import streamlit as st

# 設置環境變數
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

# 連接到 MongoDB Atlas
client = MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
db_name = "ImageDatabase"
collection_name = "ImageEmbeddings"
atlas_collection = client[db_name][collection_name]

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化模型
base_model = VGG16(weights="imagenet")
model = Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)


# 定義圖片嵌入函數
def get_image_embedding(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    vgg16_feature = model.predict(img_data)
    return vgg16_feature.flatten()


# 刪除現有數據的函數
def delete_existing_data():
    result = atlas_collection.delete_many({})
    return result.deleted_count


# 初始化數據
def initialize_data(image_folder):
    # 刪除現有數據
    delete_existing_data()

    # 遍歷資料夾中的所有圖片文件
    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(image_folder, filename)
            embedding = get_image_embedding(img_path)
            atlas_collection.insert_one(
                {"image_name": filename, "embedding": embedding.tolist()}
            )
            print(f"Inserted {filename} into the database.")


# 搜索相似圖片並顯示相似度
def search_similar_images(query_img_path):
    query_embedding = get_image_embedding(query_img_path)

    # 取得所有已儲存的向量
    stored_images = list(
        atlas_collection.find({}, {"embedding": 1, "image_name": 1, "_id": 0})
    )
    embeddings = np.array([img["embedding"] for img in stored_images])
    image_names = [img["image_name"] for img in stored_images]

    # 計算餘弦相似度
    similarity_scores = cosine_similarity([query_embedding], embeddings).flatten()
    sorted_indices = similarity_scores.argsort()[::-1]  # 按降序排列

    # 取得前5個相似的圖片及其相似度
    top_images = [(image_names[i], similarity_scores[i]) for i in sorted_indices[:5]]
    return top_images


# 顯示圖片
def display_images(query_img_path, similar_images, image_folder):
    fig, axes = plt.subplots(1, 6, figsize=(20, 5))

    # 顯示查詢圖片
    query_img = image.load_img(query_img_path, target_size=(224, 224))
    axes[0].imshow(query_img)
    axes[0].set_title("Query Image")
    axes[0].axis("off")

    # 顯示相似圖片
    for i, (img_name, similarity) in enumerate(similar_images):
        img_path = os.path.join(image_folder, img_name)
        img = image.load_img(img_path, target_size=(224, 224))
        axes[i + 1].imshow(img)
        axes[i + 1].set_title(f"{similarity:.4f}")
        axes[i + 1].axis("off")

    plt.show()


# 設置圖片文件夾路徑
image_folder = "./face_detect_done"

# 檢查集合是否為空，若為空則初始化資料
if atlas_collection.count_documents({}) == 0:
    print("初始化資料並建立向量儲存...")
    initialize_data(image_folder)
else:
    print("載入現有向量儲存...")

# 搜索相似圖片
# 更改為所要查詢圖片路徑
query_img_path = "./face_detect_source/image_01.jpg"
similar_images = search_similar_images(query_img_path)

# 顯示結果
print("相似圖片：")
for img, similarity in similar_images:
    print(f"圖片: {img}, 相似度: {similarity:.4f}")

# 顯示查詢圖片和相似圖片
display_images(query_img_path, similar_images, image_folder)
