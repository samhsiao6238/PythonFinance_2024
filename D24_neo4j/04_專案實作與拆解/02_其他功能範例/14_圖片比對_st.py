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
import streamlit as st
from PIL import Image, ImageOps

# 設置環境變數
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
ATLAS_CONNECTION_STRING = st.secrets["MONGODB_URL"]

# 連接到 MongoDB Atlas
client = MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=certifi.where())
db_name = "ImageDatabase"
collection_name = "ImageEmbeddings"
atlas_collection = client[db_name][collection_name]

# 忽略 SSL 證書驗證
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化模型
base_model = VGG16(weights="imagenet")
model = Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)


# 定義圖片嵌入函數
def get_image_embedding(img_path):
    img = Image.open(img_path)
    # 先調整短邊至224
    width, height = img.size
    if width < height:
        new_width = 224
        new_height = int(height * (224 / width))
    else:
        new_height = 224
        new_width = int(width * (224 / height))

    img = img.resize((new_width, new_height), Image.LANCZOS)
    # 再進行裁剪
    img = ImageOps.fit(img, (224, 224), Image.LANCZOS)
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)

    vgg16_feature = model.predict(img_data)
    return vgg16_feature.flatten()


# 刪除現有數據的函數
def delete_existing_data():
    result = atlas_collection.delete_many({})
    # 刪除後變更狀態
    st.session_state["data_deleted"] = True
    # 確保初始化標誌設為 False
    st.session_state["data_initialized"] = False
    return result.deleted_count


# 初始化數據
def initialize_data(image_folder):
    # 刪除現有數據
    # delete_existing_data()

    # 遍歷資料夾中的所有圖片文件
    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(image_folder, filename)
            # 檢查圖片是否已存在
            if atlas_collection.count_documents({"image_name": filename}) == 0:
                embedding = get_image_embedding(img_path)
                atlas_collection.insert_one(
                    {"image_name": filename, "embedding": embedding.tolist()}
                )
                print(f"Inserted {filename} into the database.")
    # 標記為已初始化
    st.session_state["data_initialized"] = True


# 搜索相似圖片並顯示相似度
def search_similar_images(query_img_path):
    query_embedding = get_image_embedding(query_img_path)

    # 獲取所有已儲存的向量
    stored_images = list(
        atlas_collection.find({}, {"embedding": 1, "image_name": 1, "_id": 0})
    )
    # 添加檢查是否為空的邏輯
    if len(stored_images) == 0:
        st.error("資料庫為空，無法進行相似圖片搜索。請先添加一些圖片到資料庫中。")
        return []

    embeddings = np.array([img["embedding"] for img in stored_images])
    image_names = [img["image_name"] for img in stored_images]

    # 計算餘弦相似度
    similarity_scores = cosine_similarity([query_embedding], embeddings).flatten()
    # 按降序排列
    sorted_indices = similarity_scores.argsort()[::-1]

    # 獲取前5個相似的圖片及其相似度
    top_images = [(image_names[i], similarity_scores[i]) for i in sorted_indices[:5]]
    return top_images


# 顯示圖片
def display_images(query_img_path, similar_images, image_folder):
    # 在 Streamlit 中顯示查詢圖片
    st.image(query_img_path, caption="Query Image", use_column_width=True)

    # 顯示相似圖片
    for img_name, similarity in similar_images:
        img_path = os.path.join(image_folder, img_name)
        st.image(img_path, caption=f"相似度: {similarity:.4f}", use_column_width=True)


# Streamlit 應用程序
st.title("圖片相似度搜索")

# 設置圖片文件夾路徑
image_folder = "./face_detect_done"

# 檢查集合是否為空，若為空則初始化資料
if atlas_collection.count_documents({}) == 0:
    st.write("初始化資料並創建向量存儲...")
    initialize_data(image_folder)
else:
    st.write("載入現有向量存儲...")

# 確保上傳圖片的目錄存在
upload_folder = "./uploaded_images"
os.makedirs(upload_folder, exist_ok=True)

# 上傳圖片
uploaded_file = st.file_uploader("上傳圖片進行搜索", type=["png", "jpg", "jpeg"])

if st.sidebar.button("刪除所有數據"):
    delete_count = delete_existing_data()
    st.sidebar.write(f"已刪除 {delete_count} 條數據")
    # 刪除數據後重新運行應用
    st.experimental_rerun()

if "data_deleted" not in st.session_state:
    st.session_state["data_deleted"] = False

# 只有當數據未被刪除時才初始化數據
if not st.session_state["data_deleted"]:
    # 檢查集合是否為空，若為空則初始化資料
    if atlas_collection.count_documents({}) == 0:
        st.write("初始化資料並創建向量存儲...")
        initialize_data(image_folder)
    else:
        st.write("載入現有向量存儲...")

# 顯示當前資料庫中的資料筆數
data_count = atlas_collection.count_documents({})
st.sidebar.write(f"當前資料庫中的資料筆數: {data_count}")

if uploaded_file is not None:
    # 保存上傳的圖片
    query_img_path = os.path.join(upload_folder, uploaded_file.name)
    with open(query_img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 搜索相似圖片
    similar_images = search_similar_images(query_img_path)

    # 顯示結果
    st.write("相似圖片：")
    for img, similarity in similar_images:
        st.write(f"圖片: {img}, 相似度: {similarity:.4f}")

    # 顯示查詢圖片和相似圖片
    display_images(query_img_path, similar_images, image_folder)
