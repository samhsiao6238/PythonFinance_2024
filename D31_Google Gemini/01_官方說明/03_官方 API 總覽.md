# Gemini API 總覽

_官方入門範例和 API 總覽的內容進行篩選和補充，重複部分不再說明；另外部分官方教程上有錯誤，以下皆已進行修正。_

![](images/img_07.png)

<br>

## 簡單範例

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

    # 設置 API 金鑰，請更改為自己的實際金鑰
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    # 配置 Google API 使用自己的金鑰
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

    _結果_

    ```bash
    看起來是買來的。
    ```

<br>

3. 換一張看起來比較平實的相片。

    <img src="images/img_06.png" width="300px" />

    _結果_

    ```bash
    這些看起來是自製的。
    ```

<br>

4. 使用流式方式取得生成內容。

    ```python
    # 定義提示文本
    prompt = """
    你是一個風趣的文學大師。
    請以繁體中文講一個關於神奇背包的故事。
    """

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

    _回答：_

    ```bash
    話
    說江湖上有一位名叫「背包俠」的奇人，他背
    上永遠背著一個平凡無奇的帆布背包。但這個背包
    卻有著不平凡的秘密，它有著「七十二變」的奇特能力！ 

    背包俠是個愛好旅行的浪子，走到
    哪就背著它到哪。有一天，他來到一個荒涼的沙漠，口渴難耐，眼看就要渴死。正當他
    絕望之際，他拍了拍背包，輕輕地說：「給我一杯清涼的泉水。」話音剛落，背包裡竟然就冒出一個精緻的玉杯，盛滿了晶瑩剔透的
    泉水！背包俠欣喜若狂，一飲而盡，顿时神清氣爽。

    他又繼續向前走，遇見了一條湍急的河流。他想要過河，卻沒有船隻。這時
    ，他再次拍了拍背包，說：「給我一條堅固的木橋。」眨眼間，背包裡竟伸出了一條精緻的木橋，跨越了河流。背包俠順利地走過了河流，心中充滿了驚奇。

    他還用背包變出過金銀財寶，
    用它治癒過病人，甚至用它從凶猛的野獸手中救過人！他一路行俠仗義，用背包幫助了無數人，成為江湖上傳奇般的存在。

    後來，背包俠漸漸老去，他將背包交給了一個善良的少年，
    希望他也能像自己一樣，用背包幫助更多的人。少年接過背包，懷著滿腔熱血，踏上了新的旅程。

    背包俠的故事就這樣一代代流傳下來，成為了一個充滿奇幻色彩的傳說。它告訴我們，看似平凡的事物，可能蘊藏
    著無限的可能，只要你用心去發現，就會有驚喜出現。

    當然，這個故事也讓我們明白，擁有神奇的背包固然重要，但更重要的是擁有善良的心和樂於助人的精神，才能真正地幫助他人，讓世界變得更美好。

    完整生成內容：
    話說江湖上有一位名叫「背包俠」的奇人，他背上永遠背著一個平凡無奇的帆布背包。但這個背包卻有著不平凡的秘密，它有著「七十二變」的奇特能力！ 

    背包俠是個愛好旅行的浪子，走到哪就背著它到哪。有一天，他來到一個荒涼的沙漠，口渴難耐，眼看就要渴死。正當他絕望之際，他拍了拍背包，輕輕地說：「給我一杯清涼的泉水。」話音剛落，背包裡竟然就冒出一個精緻的玉杯，盛滿了晶瑩剔透的泉水！背包俠欣喜若狂，一飲而盡，顿时神清氣爽。

    他又繼續向前走，遇見了一條湍急的河流。他想要過河，卻沒有船隻。這時，他再次拍了拍背包，說：「給我一條堅固的木橋。」眨眼間，背包裡竟伸出了一條精緻的木橋，跨越了河流。背包俠順利地走過了河流，心中充滿了驚奇。

    他還用背包變出過金銀財寶，用它治癒過病人，甚至用它從凶猛的野獸手中救過人！他一路行俠仗義，用背包幫助了無數人，成為江湖上傳奇般的存在。

    後來，背包俠漸漸老去，他將背包交給了一個善良的少年，希望他也能像自己一樣，用背包幫助更多的人。少年接過背包，懷著滿腔熱血，踏上了新的旅程。

    背包俠的故事就這樣一代代流傳下來，成為了一個充滿奇幻色彩的傳說。它告訴我們，看似平凡的事物，可能蘊藏著無限的可能，只要你用心去發現，就會有驚喜出現。

    當然，這個故事也讓我們明白，擁有神奇的背包固然重要，但更重要的是擁有善良的心和樂於助人的精神，才能真正地幫助他人，讓世界變得更美好。
    ```

<br>

5. 設定返回 JSON 格式回應。

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

    _結果_

    ```bash
    [
        {"recipe_name": "巧克力餅乾"}, {"recipe_name": "燕麥餅乾"}, {"recipe_name": "花生醬餅乾"}, {"recipe_name": "薑餅乾"}, {"recipe_name": "砂糖餅乾"}
    ]

    格式化後的 JSON 數據:
    [
        {
            "recipe_name": "巧克力餅乾"
        },
        {
            "recipe_name": "燕麥餅乾"
        },
        {
            "recipe_name": "花生醬餅乾"
        },
        {
            "recipe_name": "薑餅乾"
        },
        {
            "recipe_name": "砂糖餅乾"
        }
    ]
    ```

<br>

## 受控生成 / 約束解碼

_controlled generation、constrained decoding_

1. `Gemini 1.5 Flash` 和 `Gemini 1.5 Pro` 模型在處理 JSON Schema 的方法不同，`Gemini 1.5 Flash` 僅接受 `JSON Schema 的文本描述`；而 `Gemini 1.5 Pro` 模型允許傳遞一個 `JSON Schema 對象` 或 `Python 類`，並且模型輸出將嚴格遵循該 Schema，這稱為 `受控生成（controlled generation）`或 `約束解碼（constrained decoding）`，這是一種根據特定的結構和格式生成內容，確保生成的結果符合預定的規範。

<br>

2. 使用 `受控生成` 進行 JSON 返回。

    ```python
    # 導入 typing_extensions 用於定義型別
    import typing_extensions as typing

    # 定義 JSON 結構
    class Recipe(typing.TypedDict):
        # 定義食譜名稱欄位
        recipe_name: str

    # 初始化模型：必須使用 `gemini-1.5-pro`
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

    # 解析生成的 JSON 文本
    try:
        # 將 JSON 文本轉換為 Python 對象
        json_data = json.loads(result.text)
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

    _輸出_

```bash
[
    {
        "recipe_name": "經典巧克力豆餅乾🍪 (無敵美味！😋😋😋！)  🔥最受歡迎的餅乾食譜！🔥  🍪🍪🍪  試試看，你會愛上它！ 💖 💖 💖 💖 💖  #餅乾 #巧克力 #食譜  https://www.example.com/chocolate-chip-cookies"
    },
    {
        "recipe_name": "酥脆燕麥葡萄乾餅乾 🍇  ✨簡單又美味！✨  💪健康又營養！💪  #餅乾 #燕麥 #葡萄乾 #食譜  https://www.example.com/oatmeal-raisin-cookies"
    },
    {
        "recipe_name": "奶油花生醬餅乾 🥜  🥜🥜🥜  經典美式風味！🇺🇸  保證讓你一口接一口！😋  #餅乾 #花生醬 #食譜  https://www.example.com/peanut-butter-cookies"
    },
    {
        "recipe_name": "雙重巧克力餅乾 🍫🍫  🍫🍫🍫  巧克力愛好者的最愛！💖  濃郁的巧克力風味！🤤  #餅乾 #巧克力 #食譜  https://www.example.com/double-chocolate-cookies"
    },
    {
        "recipe_name": "抹茶白巧克力餅乾 💚🤍  🌿🍵  獨特的日式風味！🇯🇵  香濃的抹茶與香甜的白巧克力完美結合！😍  #餅乾 #抹茶 #白巧克力 #食譜  https://www.example.com/matcha-white-chocolate-cookies"
    }
] 

格式化後的 JSON 數據:
[
    {
        "recipe_name": "經典巧克力豆餅乾🍪 (無敵美味！😋😋😋！)  🔥最受歡迎的餅乾食譜！🔥  🍪🍪🍪  試試看，你會愛上它！ 💖 💖 💖 💖 💖  #餅乾 #巧克力 #食譜  https://www.example.com/chocolate-chip-cookies"
    },
    {
        "recipe_name": "酥脆燕麥葡萄乾餅乾 🍇  ✨簡單又美味！✨  💪健康又營養！💪  #餅乾 #燕麥 #葡萄乾 #食譜  https://www.example.com/oatmeal-raisin-cookies"
    },
    {
        "recipe_name": "奶油花生醬餅乾 🥜  🥜🥜🥜  經典美式風味！🇺🇸  保證讓你一口接一口！😋  #餅乾 #花生醬 #食譜  https://www.example.com/peanut-butter-cookies"
    },
    {
        "recipe_name": "雙重巧克力餅乾 🍫🍫  🍫🍫🍫  巧克力愛好者的最愛！💖  濃郁的巧克力風味！🤤  #餅乾 #巧克力 #食譜  https://www.example.com/double-chocolate-cookies"
    },
    {
        "recipe_name": "抹茶白巧克力餅乾 💚🤍  🌿🍵  獨特的日式風味！🇯🇵  香濃的抹茶與香甜的白巧克力完美結合！😍  #餅乾 #抹茶 #白巧克力 #食譜  https://www.example.com/matcha-white-chocolate-cookies"
    }
]
```

<br>

___

_END_