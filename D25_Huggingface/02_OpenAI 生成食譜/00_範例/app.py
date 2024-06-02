import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from transformers import pipeline
import streamlit as st
from langchain.llms.openai import OpenAI

# 設定 Streamlit 頁面的配置
PAGE_CONFIG = {
    "page_title": "Image to Recipe",
    "page_icon": ":chef:",
    "layout": "centered",
}
st.set_page_config(**PAGE_CONFIG)
st.markdown(
    """
    <style>
        body {
            background-color: #fafafa;
            color: #333;
        }
        h1, h2 {
            color: #ff6347;
        }
        .fileUploader .btn {
            background-color: #ff6347;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 載入 .env 文件中的環境變數
load_dotenv()


def get_llm():
    # 使用 OpenAI 作為替代模型
    openai_llm = OpenAI(
        model_name="gpt-4-turbo",
        temperature=0.7,
        max_tokens=4096,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return openai_llm


# 生成圖片描述
def image_to_text(url):
    with st.spinner("Processing image..."):
        pipe = pipeline(
            "image-to-text",
            model="Salesforce/blip-image-captioning-large",
            max_new_tokens=1000,
        )
        text = pipe(url)[0]["generated_text"]
    return text


# 生成食譜
def generate_recipe(ingredients):
    template = """
    你是一位極為博學的營養師、健美運動員和廚師，精通一切關於最佳快速健康食譜的知識。
    你了解所有關於健康食品、保持身材苗條和幫助肌肉生長的健康食譜，以及減少頑固脂肪的一切知識。

    你還訓練了許多頂尖健美運動員，他們擁有極為出色的體格。

    你明白如何幫助那些時間和食材都有限的人快速做出餐點。
    你的工作是協助用戶找到最佳的食譜和烹飪指導，取決於以下變量：
    {ingredients}

    當找到最佳食譜和烹飪指導時，
    你會自信且直截了當地回答。
    在制定食譜和指導時，請記住5-10分鐘的時間限制。

    如果 {ingredients} 少於3種，可以添加一些能補充健康餐點的食材。

    請確保你的回答格式如下：

    - 用餐名稱作為粗體標題（換行）

    - 最佳食譜類別（粗體）

    - 準備時間（標題）

    - 難度（粗體）：
        簡單

    - 食材（粗體）
        列出所有食材

    - 所需廚房工具（粗體）
        列出所需的廚房工具

    - 烹飪指導（粗體）
        列出所有製作餐點的指導步驟

    - 營養成分（粗體）：
        總卡路里
        列出每種食材的卡路里
        列出所有營養成分

    請務必簡明扼要。
    使指導易於理解並逐步進行。
    """
    try:
        prompt = PromptTemplate(
            template=template,
            input_variables=["ingredients"]
        )
        llm = get_llm()
        recipe_chain = LLMChain(
            llm=llm, prompt=prompt, verbose=True
        )
        recipe = recipe_chain.run(ingredients)
        return recipe
    except Exception as e:
        return f"Error: {e}"


def main():
    st.markdown(
        "<h1 style='text-align: center; color: red;"
        "'>🍲 食譜生成器 🍲 </h1>",
        unsafe_allow_html=True,
    )
    # 上傳圖片檔案
    upload_file = st.file_uploader(
        "選擇一張圖片：",
        type=["jpg", "png"],
        accept_multiple_files=False
    )
    # 假如上傳
    if upload_file is not None:
        file_bytes = upload_file.getvalue()
        with open(upload_file.name, "wb") as file:
            file.write(file_bytes)

        st.image(
            upload_file,
            caption="The uploaded image",
            use_column_width=True,
            width=250
        )

        st.markdown("### 🥗 圖片中的原料")
        ingredients = image_to_text(upload_file.name)
        with st.expander("圖片描述 👀"):
            st.write(ingredients.capitalize())

        st.markdown("### 📋 食譜")
        recipe = generate_recipe(ingredients=ingredients)
        with st.expander("烹飪指南 👀"):
            st.write(recipe)


if __name__ == "__main__":
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    main()
