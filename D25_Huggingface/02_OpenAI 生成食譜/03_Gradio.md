# Gradio 

_可參考 [官方文檔](https://gradio.app/)_

<br>

## 說明

1. 是一個用於構建和分享機器學習應用的 Python 庫，它使開發者能夠輕鬆地將機器學習模型轉化為具有圖形用戶界面的應用程序，並且可以在幾行代碼內完成這一過程。

<br>

2. Gradio 的應用程序可以在本地運行，也可以通過互聯網共享，這使得它非常適合於快速原型設計和展示機器學習模型。

<br>

## 主要功能和特點

1. Gradio 的 API 非常簡單，幾乎不需要額外的設置，只需要幾行代碼就可以創建一個交互式界面。

<br>

2. 支持多種輸入格式，如文本、圖像、音頻、視頻等。輸出也可以是文本、圖像等。

<br>

3. 可以在本地測試應用，並且可以生成一個公共鏈接，讓其他人通過網頁瀏覽器來使用這個應用。

<br>

4. 非常適合用於快速原型設計和模型展示，使得研究者和開發者能夠快速測試和分享他們的機器學習模型。

<br>

## 實作

1. 安裝庫。

    ```bash
    pip install gradio transformers
    ```

<br>

2. 簡單圖像分類應用。

    ```python
    import gradio as gr
    from transformers import pipeline

    # 創建圖像分類的 pipeline
    classifier = pipeline(
        "image-classification",
        # 使用模型
        model="google/vit-base-patch16-224"
    )


    # 定義了一個分類函數，並使用 Gradio 接口
    # 接受一個圖像輸入，並返回分類結果
    def classify_image(image):
        result = classifier(image)
        return {item['label']: item['score'] for item in result}

    # 使用 Gradio 創建 Web 界面
    # 通過 `gr.Interface` 函數將分類函數與界面元素（圖像輸入和標籤輸出）綁定
    gr.Interface(
        fn=classify_image,
        inputs="image",
        outputs="label"
    ).launch()
    ```

<br>

## 產生公共鏈接

1. 要使其他人能夠訪問 Gradio 應用，可以在 launch() 方法中設定 share=True 參數，這樣 Gradio 會為應用程式產生一個臨時的公共鏈接與他人分享。

    ```python
    import gradio as gr
    from transformers import pipeline

    # 建立影像分類的 pipeline
    classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

    # 分類函數
    def classify_image(image):
        result = classifier(image)
        return {item['label']: item['score'] for item in result}

    # 使用 Gradio 建立 Web 介面並產生公共鏈接
    gr.Interface(
        fn=classify_image,
        inputs="image",
        outputs="label"
    ).launch(share=True)
    ```

<br>

___

_END_