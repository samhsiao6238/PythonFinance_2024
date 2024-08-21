# Streamlit 專案

_部署訓練好的情感分析模型到 Hugging Face 的 `Space`，並建立一個簡單的網頁應用，讓用戶可以在線輸入文本並得到情感分析結果。_

<br>

## 建立 Streamlit 專案

_在本地建立一個 Streamlit 專案，用來展示情感分析模型_

<br>

1. 建立一個新的目錄，並進入該目錄。

    ```bash
    mkdir st_sentiment_app && cd st_sentiment_app
    ```

<br>

2. 建立並啟用虛擬環境，細節省略。

    ```bash
    python -m venv envHuggingface
    ```

<br>

3. 安裝所需的依賴項，包括 `streamlit` 和 `transformers`。

    ```bash
    pip install streamlit transformers
    ```

<br>

## Streamlit 應用

1. 建立並編輯專案主腳本 `app.py`。

    ```python
    # app.py

    import streamlit as st
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch

    # 載入模型和分詞器
    tokenizer = AutoTokenizer.from_pretrained("username/chinese-sentiment-model")
    model = AutoModelForSequenceClassification.from_pretrained("username/chinese-sentiment-model")

    st.title("中文情感分析")
    st.write("這是一個基於 BERT 的中文情感分析模型。請輸入一段文本來分析其情感。")

    # 輸入框
    user_input = st.text_area("輸入中文文本:")

    if st.button("分析"):
        # 處理輸入文本
        inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
        outputs = model(inputs)

        # 獲得預測結果
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        label_map = ["負面", "中性", "正面"]
        predicted_label = label_map[predictions.argmax().item()]

        st.write(f"模型預測的情感為：{predicted_label}")

    ```

<br>

2. 在本地測試 Streamlit 應用程式。

    ```bash
    streamlit run app.py
    ```

<br>

## 部署專案

_一旦確認應用程式運行正常，可將其部署到 Hugging Face 的 `Space`_

<br>

1. 登錄 Hugging Face，然後建立一個新的 `Space`，並選擇 `Streamlit` 作為應用的框架。

<br>

2. 編輯 `requirements.txt` 文件。

    ```json
    transformers
    streamlit
    ```

<br>

3. 將專案目錄初始化為 Git 儲存庫，然後推送到 Hugging Face 的 `Space` 儲存庫。

    ```bash
    git init
    git remote add origin https://huggingface.co/spaces/username/streamlit-sentiment-app
    git add .
    git commit -m "Initial commit"
    git push -u origin main
    ```

<br>

## 配置並運行應用

1. 推送後，Hugging Face 會自動檢測並運行 Streamlit 應用，這是一個可互動的網頁，允許用戶輸入文本並查看情感分析結果；可在 `Space` 頁面中查看應用的運行情況，並將應用連結分享給其他人。

<br>

___

_END_