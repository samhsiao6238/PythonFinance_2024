# 說明

_這個腳本是使用 `Hugging Face` 搭配 `LangChain` 製作一個 `Streamlit` 應用_

<br>

## 圖片轉文本

1. 使用 `Hugging Face` 的 `transformers` 套件和一個預訓練的模型將圖片轉換為文字說明。

<br>

2. 程式碼。

    ```python
    import os
    from dotenv import load_dotenv
    from transformers import pipeline
    from PIL import Image

    # 讀取環境變數
    load_dotenv()


    def image_to_text(image_path):
        try:
            # 使用 transformers 的 pipeline 初始化圖像到文字
            pipe = pipeline(
                # 指定任務類型為圖像到文字
                "image-to-text",
                # 使用預訓練的圖像描述模型
                model="Salesforce/blip-image-captioning-large",  
                # 設定生成文本的最大 token 數
                max_new_tokens=1000,
            )
            # 使用 PIL 庫讀取圖片
            image = Image.open(image_path)
            # 使用模型生成圖片的描述文本
            text = pipe(image)[0]["generated_text"]  
            return text
        except Exception as e:
            # 捕捉並返回任何異常錯誤
            return f"Error: {e}"

    # 測試函數
    def test_image_to_text():
        # 設定測試圖片的路徑
        # test_image_path = "麻婆豆腐.png"
        test_image_path = "棒球場.png"
        # 調用 image_to_text 函數將圖片轉換為文字
        result = image_to_text(test_image_path)
        # 結果
        print("圖像轉換為文字結果:", result)

    if __name__ == "__main__":
        # 執行
        test_image_to_text()
    ```

<br>

## 完整腳本

1. 程式碼。

    ```python
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

    # 載入環境變數
    load_dotenv()


    def get_llm():
        # 使用 OpenAI 模型
        openai_llm = OpenAI(
            model_name="gpt-4-turbo",
            temperature=0.7,
            max_tokens=4096,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        return openai_llm


    def image_to_text(url):
        with st.spinner("Processing image..."):
            pipe = pipeline(
                "image-to-text",
                model="Salesforce/blip-image-captioning-large",
                max_new_tokens=1000,
            )
            text = pipe(url)[0]["generated_text"]
        return text


    # 模板
    def generate_recipe(ingredients):
        template = """
        你是一位極為博學的營養師、健美運動員和廚師，精通一切關於最佳快速健康食譜的知識。
        你了解所有關於健康食品、保持身材苗條和幫助肌肉生長的健康食譜，以及減少頑固脂肪的一切知識。

        你還訓練了許多頂尖健美運動員，他們擁有極為出色的體格。

        你明白如何幫助那些時間和食材都有限的人快速做出餐點。
        你的工作是協助用戶找到最佳的食譜和烹飪指導，取決於以下變量：
        0/ {ingredients}

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
            recipe_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
            recipe = recipe_chain.run(ingredients)
            return recipe
        except Exception as e:
            return f"Error: {e}"


    def main():
        st.markdown(
            "<h1 style='text-align: center; color: red;'>🍲 Recipe Generator 🍲 </h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h2 style='text-align: center; font-size: 24px; color: black'>Powered by <span style='color: orange;'>OpenAI</span></h2>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <a href="https://d1nd1o4zkls5mq.cloudfront.net/img1.jpeg" target="_blank">
                    <button style="margin-right: 10px; color: white; background-color: #007BFF; border: none; border-radius: 2px; padding: 10px 15px; transition: background-color 0.3s;">
                        Download Sample Image 1
                    </button>
                </a>
                <a href="https://d1nd1o4zkls5mq.cloudfront.net/img2.jpeg" target="_blank">
                    <button style="color: white; background-color: #007BFF; border: none; border-radius: 2px; padding: 10px 15px; transition: background-color 0.3s;">
                        Download Sample Image 2
                    </button>
                </a>
            </div>
            <style>
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        upload_file = st.file_uploader(
            "Choose an image:", type=["jpg", "png"], accept_multiple_files=False
        )

        if upload_file is not None:
            file_bytes = upload_file.getvalue()
            with open(upload_file.name, "wb") as file:
                file.write(file_bytes)

            st.image(
                upload_file, caption="The uploaded image", use_column_width=True, width=250
            )

            st.markdown("### 🥗 Ingredients from Image")
            ingredients = image_to_text(upload_file.name)
            with st.expander("Ingredients 👀"):
                st.write(ingredients.capitalize())

            st.markdown("### 📋 Recipe")
            recipe = generate_recipe(ingredients=ingredients)
            with st.expander("Cooking Instructions 👀"):
                st.write(recipe)


    if __name__ == "__main__":
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        main()
    ```


<br>

___

_END_