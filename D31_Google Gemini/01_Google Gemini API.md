# Google Gemini API

<br>

## 參考 

1. [官網](https://ai.google.dev/aistudio?hl=zh-tw)。

    ![](images/img_54.png)

<br>

2. [範例文本](https://medium.com/@proflead/ai-chatbot-python-and-gemini-api-tutorial-for-beginners-c809b08bfe8c) 及 [範例 GitHub](https://github.com/proflead/gemini-flask-app/tree/master)。

<br>

## 說明 

1. 安裝套件。

    ```bash
    pip install Flask langchain-core langchain-google-genai
    ```

<br>

2. 建立環境變數。

    ```python
    os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
    ```

<br>

## 建立腳本

1. 程式碼。

    ```python
    # 導入 Streamlit 庫
    import streamlit as st

    # 導入 LangChain 的消息模塊
    from langchain_core.messages import HumanMessage
    # 導入 LangChain 與 Google Generative AI 的集成
    from langchain_google_genai import ChatGoogleGenerativeAI
    import os
    # 導入 dotenv 庫，用於加載環境變量
    from dotenv import load_dotenv

    # 加載 .env 文件中的環境變量
    load_dotenv()

    # 獲取 GEMINI_API_KEY 環境變量的值
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # 檢查 GEMINI_API_KEY 是否已經設置
    if GEMINI_API_KEY is None:
        # 如果未設置，則在 Streamlit 中顯示錯誤信息
        st.error("環境變量 GEMINI_API_KEY 未設置，請檢查 .env 文件。")
        # 停止 Streamlit 應用程序的運行
        st.stop()

    # 設置 Streamlit 應用程序的標題
    st.title("Gemini API 文本生成器")

    # 配置 Streamlit 流式輸出參數
    # 設置隊列中可保留的最大輸出數量為 10
    st.session_state.max_queued_outputs = 10
    # 設置輸出生成之間的間隔時間為 0.5 秒
    st.session_state.report_interval = 0.5
    # 設置為非按需生成輸出
    st.session_state.on_demand = False

    # 創建一個文本輸入框供用戶輸入問題
    user_input = st.text_input("在此輸入問題：")

    # 當用戶點擊“產生”按鈕時執行的操作
    if st.button("產生"):
        try:
            # 檢查用戶是否輸入了文本
            if not user_input:
                # 如果未輸入，則顯示警告信息
                st.warning("請輸入一些說明。")
            else:
                # 設置模型名稱為 gemini-pro
                model_name = "gemini-pro"
                # 創建 ChatGoogleGenerativeAI 模型實例，並傳入模型名稱和 API 密鑰
                model = ChatGoogleGenerativeAI(
                    model=model_name, google_api_key=GEMINI_API_KEY
                )
                # 創建 HumanMessage 實例，將用戶輸入作為消息內容
                message = HumanMessage(content=user_input)
                # 使用模型的 stream 方法生成文本
                response = model.stream([message])

                # 創建一個空的 Streamlit 元素，以便後續更新輸出
                output_placeholder = st.empty()
                # 初始化生成的文本字符串
                generated_text = ""

                # 使用流式方式逐步顯示生成的文本
                for chunk in response:
                    # 將每個生成的文本塊添加到生成的文本中
                    generated_text += chunk.content
                    # 使用 Streamlit 更新文本顯示，實時顯示生成的文本
                    output_placeholder.text(generated_text)

                # 顯示成功信息，指示文本生成完成
                st.success("生成文字已完成。")

        # 捕獲和處理生成文本過程中的異常
        except Exception as e:
            # 顯示錯誤信息
            st.error(f"發生錯誤： {str(e)}")
    ```

<br>

2. 運行。

    ```bash
    streamlit run app.py
    ```

<br>

___

_END_