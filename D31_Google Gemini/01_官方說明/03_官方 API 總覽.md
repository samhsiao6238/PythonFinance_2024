# Gemini API 總覽

_官方入門範例和 API 總覽的內容進行篩選和補充，這個部分在官方教程上有許多錯誤，以下會進行修正。_

<br>

## API 總覽

1. 使用一張圖片 `cookie.png` 並對模型提問 `這些看起來是買來的還是自製的？`。

    <img src="images/img_05.png" width="300px" />

<br>

2. 使用模型進行多模態提示。

    ```python
    # 用於處理文件路徑
    import pathlib
    # 導入 Google Gemini API 的 SDK
    import google.generativeai as genai
    import PIL.Image  # 用於讀取圖片
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # 設置 API 金鑰，請替換為您的實際金鑰
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    # 配置 Google API 使用您的金鑰
    genai.configure(api_key=GOOGLE_API_KEY)

    # 初始化模型，這裡使用 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 讀取圖片文件並建立一個 PIL Image 對象
    image_path = 'cookie.png'
    image = PIL.Image.open(image_path)

    # 提示文本，說明你希望模型進行的操作
    prompt = "這些看起來是買來的還是自製的？"

    # 使用多模態輸入生成內容
    response = model.generate_content(
        # 包含文本和圖片的內容
        contents=[prompt, image],
        # 啟用流式輸出，允許逐步生成回應
        stream=True
    )

    # 確保所有流式回應塊都已處理完畢
    full_text = ""
    for chunk in response:
        # 累積生成的文本塊
        full_text += chunk.text

    # 輸出最終生成的文本
    print(full_text)
    ```

<br>

3. 使用流式方式取得生成內容。

    ```python
    # 定義提示文本
    prompt = "講一個關於神奇背包的故事。"

    # 使用流式方式取得生成內容
    response = model.generate_content(
        # 傳遞提示文本
        contents=prompt,
        # 啟用流式輸出，允許逐步生成回應
        stream=True
    )

    # 確保所有流式回應塊都已處理完畢
    full_text = ""
    for chunk in response:
        # 累積生成的文本塊
        full_text += chunk.text
        # 輸出每個內容塊的文本
        print(chunk.text)

    # 輸出最終生成的文本
    print("完整生成內容：")
    print(full_text)
    ```

<br>

3. 設定返回 JSON 格式回應。

    ```python
    # 用於解析 JSON
    import json

    # 設定回應為 JSON 格式
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        generation_config={
            "response_mime_type": "application/json"
        }
    )
    # 定義提示文本，指定返回 JSON 結構
    prompt = """
    列出5個熱門的餅乾食譜。
    使用這個 JSON 結構：
        Recipe = {"recipe_name": str}
        return `list[Recipe]`
    """
    # 使用模型生成內容
    response = model.generate_content(prompt)
    # 輸出生成的 JSON 文本
    print(response.text)
    # 解析生成的 JSON 文本
    try:
        # 將 JSON 文本轉換為 Python 對象
        json_data = json.loads(response.text)
        print("\n格式化後的 JSON 數據:")
        # 格式化並輸出 JSON 數據
        print(json.dumps(
            json_data,
            indent=4,
            ensure_ascii=False
        ))
    except json.JSONDecodeError as e:
        print(f"無法解析 JSON: {e}")
    ```

<br>

4. 使用受控生成進行 JSON 返回。

    ```python
    # 導入 typing_extensions 用於定義型別
    import typing_extensions as typing

    # 定義 JSON 結構
    class Recipe(typing.TypedDict):
        # 定義食譜名稱字段
        recipe_name: str

    # 初始化高級模型
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro"
    )

    result = model.generate_content(
        # 提示文本
        "列出5個熱門的餅乾食譜",  
        # 設定返回的 JSON 結構
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=list[Recipe]
        )
    )
    # 輸出生成的 JSON 文本
    print(result.text)
    ```

<br>

___

_END_