import os
from dotenv import load_dotenv
# 用於生成提示模板
from langchain_core.prompts import PromptTemplate
# 用於生成各種自然語言處理管道
from transformers import pipeline
import streamlit as st
# 用於連接 Amazon Bedrock
from langchain_aws import BedrockLLM
# 導入翻譯函數
from googletrans import Translator

# 環境參數
load_dotenv()

# 初始化翻譯器
translator = Translator()


# 定義函數以取得大語言模型
def get_llm():
    bedrock_llm = BedrockLLM(
        model_id="anthropic.claude-v2",
        region_name=os.getenv("AWS_REGION"),
        model_kwargs={"temperature": 0.7, "max_tokens_to_sample": 4096},
    )
    return bedrock_llm


# 定義函數將圖像轉換為文字
def image_to_text(url):
    # 顯示處理中的提示
    with st.spinner("Processing image..."):
        pipe = pipeline(
            "image-to-text",
            model="Salesforce/blip-image-captioning-large",
            max_new_tokens=1000,
        )
        # 取得圖像生成的文字
        text = pipe(url)[0]["generated_text"]
    # 返回生成的文字
    return text


# 定義函數生成食譜
def generate_recipe(ingredients):
    template = """
    你是一位極為博學的營養師、健美運動員和廚師，精通一切關於最佳快速健康食譜的知識。
    你了解所有關於健康食品、保持身材苗條和幫助肌肉生長的健康食譜，以及減少頑固脂肪的一切知識。
    你還訓練了許多頂尖健美運動員，他們擁有極為出色的體格。
    你明白如何幫助那些時間和食材都有限的人快速做出餐點。
    你的工作是協助用戶找到最佳的食譜和烹飪指導，取決於以下變數：
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

    with st.spinner("Making the recipe for you..."):
        prompt = PromptTemplate(
            template=template, input_variables=["ingredients"]
        )
        llm = get_llm()
        recipe_chain = prompt | llm
        recipe = recipe_chain.invoke({"ingredients": ingredients})

    return recipe


def main():

    st.markdown(
        "<h1 style='text-align: center; color: red;'>"
        "🍲 Recipe Generator 🍲 </h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<h2 style='text-align: center; font-size: 24px;"
        " color: white'>使用&nbsp;&nbsp;<span style='color: orange;'>"
        "Amazon Bedrock</span></h2>",
        unsafe_allow_html=True,
    )

    upload_file = st.file_uploader(
        "選擇圖片：",
        type=["jpg", "png"],
        accept_multiple_files=False
    )

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

        st.markdown("### 🥗 相片中的原料")
        ingredients = image_to_text(upload_file.name)
        ingredients_zh = translator.translate(
            ingredients, src='en', dest='zh-tw').text
        with st.expander("原料 👀"):
            # st.write(ingredients.capitalize())
            st.write(ingredients_zh)

        st.markdown("### 📋 食譜")
        recipe = generate_recipe(ingredients=ingredients)
        with st.expander("烹飪說明 👀"):
            st.write(recipe)

        os.remove(upload_file.name)


if __name__ == "__main__":
    load_dotenv()
    main()
