# OpenAI 入門

_先簡介主要套件 OpenAI_

<br>

## 基本說明

1. 可參考 OpenAI 的 [官方說明](https://platform.openai.com/docs/api-reference?lang=python)，或是 [GitHub 說明](https://github.com/openai/openai-python?tab=readme-ov-file)。

<br>

2. 在官方 GitHub 上提到 `api_key` 預設是讀取環境參數中 `OPENAI_API_KEY` 的鍵值，所以可透過寫入環境參數來進行設定，如此在代碼中可以不用再寫。

    ```python
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    ```

<br>

3. 參數 `model` 可在客戶端初始化時設置，也可在 API 具體調用函數時設置，這樣的設計是因應不同的 API 在調用時，可透過編程以使用不同的模型，當有這樣的需求時，可在具體調用時再指定 `model`。

    _全局設置_
    ```python
    # 統一設置
    client = OpenAI(
        api_key='YOUR_API_KEY',
        model='gpt-4-turbo',  # 統一設置模型
        organization='YOUR_ORG_ID',
        project='YOUR_PROJECT_ID',
    )
    # 在調用時不需要再次設置模型
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    ```

    _局部設置_
    ```python
    # 針對性設置
    client = OpenAI(
        api_key='YOUR_API_KEY',
        organization='YOUR_ORG_ID',
        project='YOUR_PROJECT_ID',
    )
    # 在每次調用時設置不同的模型
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # 針對此請求設置模型
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    ```

<br>

4. 延續上一點說明，所以在官方文件中，一開始並未說明 `api_key` 與 `model` 參數，僅示範 `organization` 與 `project` 這兩個用於 `組織和項目管理` 附加信息的參數。

    ```python
    from openai import OpenAI

    client = OpenAI(
    organization='YOUR_ORG_ID',
    project='$PROJECT_ID',
    )
    ```

<br>

## Streaming

1. OpenAI API 提供了 Streaming 功能，允許在某些請求中逐步返回部分結果，包含 `Chat Completions API` 與 `Assistants API`。

    ```python
    # 引入 OpenAI 模組
    from openai import OpenAI
    # 創建 OpenAI 客戶端
    client = OpenAI()

    # 發送 Streaming 請求
    stream = client.chat.completions.create(
        # 指定使用的模型
        model="gpt-4-turbo",
        # 輸入的消息
        messages=[{"role": "user", "content": "Say this is a test"}],
        # 啟用流式傳輸
        stream=True
    )

    # 遍歷流中的數據塊
    for chunk in stream:
        # 檢查 delta.content 是否為 None
        if chunk.choices[0].delta.content is not None:
            # 打印每個數據塊的內容
            print(chunk.choices[0].delta.content, end="")
    ```

<br>

## Audio

_[Text-to-speech 語音轉文字](https://platform.openai.com/docs/guides/text-to-speech)_

<br>

1. 輸入文本：提供需要轉換為語音的文本內容。

2. 選擇模型和語音：選擇要使用的 TTS 模型，如 `tts-1` ，選擇要使用的語音，如 `alloy`。

3. 生成語音：調用 API 將文本轉換為語音。

4. 輸出格式：選擇音頻的輸出格式（默認為 MP3，但也支持其他格式如 opus、aac、flac、wav、pcm）。

5. 保存或播放：將生成的音頻文件保存或實時播放。

6. 範例。

    ```python
    from pathlib import Path
    from openai import OpenAI

    # 初始化 OpenAI 客戶端
    client = OpenAI(api_key="YOUR_API_KEY")

    # 設定保存音頻文件的路徑
    speech_file_path = Path(__file__).parent / "speech.mp3"

    # 調用 API 將文本轉換為語音
    response = client.audio.speech.create(
    # 使用的 TTS 模型
    model="tts-1",
    # 使用的語音
    voice="alloy",
    # 要轉換的文本
    input="今天是個美好的日子，因為我要去見個重要的人。"
    )

    # 將生成的音頻流保存為 MP3 文件
    response.stream_to_file(speech_file_path)
    ```

<br>

_[Speech-to-text 語音轉文字](https://platform.openai.com/docs/guides/speech-to-text)_

<br>

1. 腳本。

    ```python
    from openai import OpenAI
    client = OpenAI()

    audio_file= open("audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)
    ```

<br>

2. 預設輸出為 `JSON` 文件。

    ```json
    {
        "text": "Imagine the wildest idea that you've ever had, and you're curious about how it might scale to something that's a 100, a 1,000 times bigger."
    }
    ```

<br>

3. 可加入參數來指定輸出為其他格式如 `Text`。

    ```python
    from openai import OpenAI
    client = OpenAI()

    audio_file = open("/path/to/file/speech.mp3", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    print(transcription.text)
    ```

<br>

## Chat

_可參考 [Chat Completions API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api)_

<br>

1. 在官方的說明中，可透過 `messages` 將多輪對話傳給 API 來進行下一次的對話回應。

    ```python
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # 一系列消息，每條消息都有一個角色（role）和內容（content）
        messages=[
            # system：系統消息，用於設定助理的角色和行為，這裡告訴助理要扮演的是 `有幫助的助手`
            {"role": "system", "content": "You are a helpful assistant."},
            # user：用戶消息，表示用戶的輸入
            {"role": "user", "content": "Who won the world series in 2020?"},
            # assistant：助理消息，表示助理的回應
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    ```

<br>

2. 具體示範如何使用 OpenAI 的 `Chat Completions API` 來實現多輪對話，通過收集用戶和助理之間的對話，並將這些對話傳遞給 API 來實現連續的對話溝通，這可應用於構建智能客服系統、虛擬助手等場景。

    ```python
    from openai import OpenAI
    # 創建 OpenAI 客戶端
    client = OpenAI(api_key='YOUR_API_KEY')

    # 初始化對話列表
    messages = [
        # 系統消息，用於設定助理的角色
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    # 假設這是第一次用戶輸入
    user_input = "哪支球隊贏得 2020 年世界杯？"
    # 添加用戶消息到對話列表
    messages.append({"role": "user", "content": user_input})

    # 調用 API 獲取助理回應
    response = client.chat.completions.create(
        # 指定使用的模型
        model="gpt-4-turbo",
        # 將對話列表傳遞給 API
        messages=messages
    )

    # 解析助理的回應
    assistant_response = response.choices[0].message['content']
    print(assistant_response)  # 顯示助理的回應

    # 添加助理的回應到對話列表
    messages.append({"role": "assistant", "content": assistant_response})

    # 假設這是第二次用戶輸入
    user_input = "Where was it played?"
    messages.append({"role": "user", "content": user_input})  # 添加用戶消息到對話列表

    # 再次調用 API 獲取助理回應
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 解析助理的回應
    # 特別注意，在 Python 中也可以表達為 `choices[0]["message"]["content"]`
    assistant_response = response.choices[0].message['content']
    # 顯示助理的回應
    print(assistant_response)
    # 添加助理的回應到對話列表，這時要將
    messages.append({"role": "assistant", "content": assistant_response})
    # 繼續這個流程來處理更多的用戶輸入和助理回應...
    ```

<br>

3. 補充說明 `choices[0]` 這個回應列表，其中包含一個以上模型生成的可能回應，通常情況下透過 `[0]` 取回第一個作為回應，格式如下。

    ```json
    {
        "id": "cmpl-6YB1j12345",
        "object": "text_completion",
        "created": 1614639685,
        "model": "gpt-4-turbo",
        "choices": [{
            // index：該選項在列表中的位置
            "index": 0,
            // 生成的消息，包含 role 和 content。
            "message": {
                "role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020."
            },
            // 模型停止生成的原因
            "finish_reason": "stop"
        }]
    }
    ```

<br>

## Embeddings 嵌入

1. `Embeddings` 是將文本或其他類型數據轉換為數字向量的技術，這些向量可用於捕捉文本之間的相關性，也就是將高維度、非結構化數據轉換為低維度、結構化的向量，常用於搜索、聚類、推薦、異常檢測、多樣性測量和分類等。

<br>

2. OpenAI 提供了兩個第三代嵌入模型 `text-embedding-3-small` 和 `text-embedding-3-large` 供選擇使用。

<br>

3. 使用 OpenAI 提供的 API 獲取文本嵌入，並將嵌入結果保存到文件或數據框中以便進行後續分析，這些技術和工具可以幫助開發者更好地理解和處理自然語言數據，實現各種智能應用。

<br>

4. 範例：具體展示獲取文本嵌入

    ```python
    from openai import OpenAI
    import pandas as pd
    import numpy as np
    from dotenv import load_dotenv
    import os

    # 加載環境變量
    load_dotenv()

    # 從環境變量中獲取 API 密鑰
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input=[text], model=model).data[0].embedding

    # 假設有一個包含文本數據的 DataFrame
    df = pd.DataFrame({
        'combined': [
            'Good Quality Dog Food. I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product better than most.',
            'Not as Advertised. Product arrived labeled as Jumbo Salted Peanuts...the peanuts were actually small sized unsalted. The vendor refused to refund my purchase or send me the correct product.',
            'Delicious. These are the best cookies I have ever eaten! I highly recommend them to anyone who loves chocolate.',
            'Terrible customer service. The product was okay, but the customer service was terrible. I will not be buying from this company again.',
            'Just okay. The product was neither great nor bad. It was just okay. I might buy it again if there are no better options.',
        ]
    })

    # 將文本轉換為嵌入
    df['embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-3-small'))

    # 保存結果到 CSV 文件
    df.to_csv('output/embedded_reviews.csv', index=False)

    # 從保存的文件中加載嵌入數據
    df = pd.read_csv('output/embedded_reviews.csv')
    df['embedding'] = df.embedding.apply(eval).apply(np.array)

    # 顯示結果
    print(df.head())

    ```
    _輸出_
    ```bash
                                                combined  \
    0  Good Quality Dog Food. I have bought several o...   
    1  Not as Advertised. Product arrived labeled as ...   
    2  Delicious. These are the best cookies I have e...   
    3  Terrible customer service. The product was oka...   
    4  Just okay. The product was neither great nor b...   

                                            embedding  
    0  [0.015021142549812794, -0.007734853308647871, ...  
    1  [-0.014828150160610676, -0.005706844385713339,...  
    2  [0.03156798705458641, -0.06490229815244675, -0...  
    3  [-0.03399420902132988, -0.01097179763019085, -...  
    4  [-0.04210306704044342, 0.019184265285730362, -...
    ```

<br>

## 進階用法

1. 搜尋 Search：根據查詢字串找到最相關的文本，通過計算嵌入向量之間的餘弦相似度來實現。

    ```python
    import numpy as np

    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input=[text], model=model).data[0].embedding

    def find_similar_reviews(query, df, model="text-embedding-3-small"):
        query_embedding = get_embedding(query, model=model)
        df['similarity'] = df.embedding.apply(lambda x: np.dot(query_embedding, x) / (np.linalg.norm(query_embedding) * np.linalg.norm(x)))
        similar_reviews = df.sort_values('similarity', ascending=False)
        return similar_reviews

    # 查詢示例
    query = "best cookies"
    similar_reviews = find_similar_reviews(query, df)
    print(similar_reviews[['combined', 'similarity']])
    ```
    _結果_
    ```bash
                                                combined  similarity
    2  Delicious. These are the best cookies I have e...    0.545966
    0  Good Quality Dog Food. I have bought several o...    0.195261
    1  Not as Advertised. Product arrived labeled as ...    0.129095
    4  Just okay. The product was neither great nor b...    0.079523
    3  Terrible customer service. The product was oka...    0.065597
    ```

<br>

2. 聚類 Clustering：將相似的文本分組，以使用 `K-means` 或 `DBSCAN` 等算法來實現；另外需安裝套件 `scikit-learn`。

    ```python
    from sklearn.cluster import KMeans

    # 假設 df 中的嵌入向量列名為 'embedding'
    embeddings = np.array(df['embedding'].tolist())
    kmeans = KMeans(n_clusters=3, random_state=0).fit(embeddings)
    df['cluster'] = kmeans.labels_

    print(df[['combined', 'cluster']])
    ```
    _結果_
    ```bash
                                                combined  cluster
    0  Good Quality Dog Food. I have bought several o...        0
    1  Not as Advertised. Product arrived labeled as ...        2
    2  Delicious. These are the best cookies I have e...        0
    3  Terrible customer service. The product was oka...        1
    4  Just okay. The product was neither great nor b...        1
    ```

<br>

3. 推薦 Recommendations：根據用戶的興趣推薦相似的內容，可以使用餘弦相似度來實現。

    ```python
    def recommend_similar_items(item_index, df):
        item_embedding = df.iloc[item_index]['embedding']
        df['similarity'] = df.embedding.apply(lambda x: np.dot(item_embedding, x) / (np.linalg.norm(item_embedding) * np.linalg.norm(x)))
        recommended_items = df.sort_values('similarity', ascending=False)
        return recommended_items

    # 假設推薦與第一條評論相似的項目
    recommended_items = recommend_similar_items(0, df)
    print(recommended_items[['combined', 'similarity']])

    ```
    _結果_
    ```bash
                                                combined  similarity
    0  Good Quality Dog Food. I have bought several o...    1.000000
    4  Just okay. The product was neither great nor b...    0.240480
    2  Delicious. These are the best cookies I have e...    0.199340
    1  Not as Advertised. Product arrived labeled as ...    0.164630
    3  Terrible customer service. The product was oka...    0.123355
    ```

<br>

4. 異常檢測 Anomaly Detection：識別與大多數文本不同的異常點，可以使用 Isolation Forest 或 One-Class SVM 來實現。

    ```python
    from sklearn.ensemble import IsolationForest

    embeddings = np.array(df['embedding'].tolist())
    clf = IsolationForest(random_state=0).fit(embeddings)
    df['anomaly_score'] = clf.decision_function(embeddings)
    df['anomaly'] = clf.predict(embeddings)

    print(df[['combined', 'anomaly', 'anomaly_score']])

    ```
    _結果_
    ```bash
                                                combined  anomaly  anomaly_score
    0  Good Quality Dog Food. I have bought several o...        1       0.034910
    1  Not as Advertised. Product arrived labeled as ...        1       0.040418
    2  Delicious. These are the best cookies I have e...        1       0.017985
    3  Terrible customer service. The product was oka...        1       0.036293
    4  Just okay. The product was neither great nor b...        1       0.055233
    ```

<br>

5. 多樣性測量 Diversity Measurement：分析文本之間的相似性分佈，可以通過計算嵌入向量之間的距離分佈來實現。

    ```python
    from scipy.spatial.distance import pdist, squareform

    embeddings = np.array(df['embedding'].tolist())
    distance_matrix = squareform(pdist(embeddings, metric='cosine'))

    print("Distance Matrix:\n", distance_matrix)

    ```
    _結果_
    ```bash
    Distance Matrix:
    [[0.         0.8353697  0.80065967 0.87664512 0.75951974]
    [0.8353697  0.         0.88520441 0.62127699 0.73445364]
    [0.80065967 0.88520441 0.         0.88961617 0.88532285]
    [0.87664512 0.62127699 0.88961617 0.         0.4774982 ]
    [0.75951974 0.73445364 0.88532285 0.4774982  0.        ]]
    ```

<br>

6. 分類 Classification：根據最相似的標籤對文本進行分類，可以使用邏輯回歸、支持向量機或神經網絡等分類器來實現；為 DataFrame 添加一個 label 列，可以用來標記每個評論的情感，比如 `正面（1）` 或`負面（0）`。

    ```python
    from openai import OpenAI
    import pandas as pd
    import numpy as np
    from dotenv import load_dotenv
    import os
    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report

    # 加載環境變量
    load_dotenv()

    # 從環境變量中獲取 API 密鑰
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    def get_embedding(text, model="text-embedding-3-small"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input=[text], model=model).data[0].embedding

    # 增加更多的訓練數據
    df = pd.DataFrame({
        'combined': [
            '優質狗糧。 我買了幾款 Vitality 罐裝狗糧產品，發現它們的品質都很好。 該產品看起來更像是燉菜，而不是加工過的肉，而且味道更好。 我的拉布拉多很挑剔，她比大多數人都更欣賞這個產品。',
            '不像廣告中那樣。 產品到達時標記為巨型鹹花生……花生實際上是小尺寸的未加鹽的。 供應商拒絕退還我購買的商品或向我發送正確的產品。',
            '可口的。 這是我吃過的最好的餅乾！ 我強烈推薦給所有喜歡巧克力的人。',
            '糟糕的客戶服務。 產品還可以，但客戶服務很糟糕。 我不會再從這家公司購買產品。',
            '就這樣吧。 該產品既不好也不壞。 沒關係。 如果沒有更好的選擇，我可能會再次購買。',
            '非常滿意的購物體驗。 產品質量很高，物流也很快。',
            '糟糕的產品質量。 產品不到一周就壞了，我很失望。',
            '超級好吃的零食。 每次吃都讓我很開心，真是太棒了。',
            '客戶服務非常棒。 他們非常熱心，解決了我的所有問題。',
            '我很失望。 產品與描述不符，我不會再購買了。',
            '這是我吃過的最好的一頓飯。 我真的很喜歡。',
            '這是我見過的最糟糕的產品。 我再也不會買了。',
            '味道很好。 我會再次購買。',
            '質量很差。 我很不滿意。'
        ],
        'label': [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0]  # 添加更多的標籤：1 表示正面評論，0 表示負面評論
    })

    # 將文本轉換為嵌入
    df['embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-3-small'))

    # 分割數據集為訓練集和測試集
    X = np.array(df['embedding'].tolist())
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 使用邏輯回歸進行分類
    clf = LogisticRegression(random_state=0)
    # 使用交叉驗證來評估模型性能，使用 StratifiedKFold 來確保每個折中的類別分布均勻
    cv = StratifiedKFold(n_splits=3)
    cv_scores = cross_val_score(clf, X_train, y_train, cv=cv)
    print("交叉驗證分數: ", cv_scores)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # 顯示分類報告
    print(classification_report(y_test, y_pred))

    # 定義一個函數來預測新文本的分類
    def classify_new_text(text):
        # 將新文本轉換為嵌入
        embedding = get_embedding(text, model='text-embedding-3-small')
        # 使用訓練好的模型進行預測
        prediction = clf.predict([embedding])
        return prediction[0]

    # 新文本示例
    # new_text_1 = "這款產品真的很棒，我會再次購買。"
    new_text_1 = "我覺得這款產品還不錯耶。"
    # new_text_0 = "這款產品真的不太好，我不會再買了。"
    new_text_0 = "這款產品有點讓人不太滿意。"
    predicted_label_1 = classify_new_text(new_text_1)
    predicted_label_0 = classify_new_text(new_text_0)
    print(f"新文本的預測標籤為: {predicted_label_1}")
    print(f"新文本的預測標籤為: {predicted_label_0}")

    ```
    _結果_
    ```bash
    交叉驗證分數:  [0.5 0.5 1. ]
                precision    recall  f1-score   support

            0       1.00      1.00      1.00         2
            1       1.00      1.00      1.00         1

        accuracy                           1.00         3
    macro avg       1.00      1.00      1.00         3
    weighted avg       1.00      1.00      1.00         3

    新文本的預測標籤為: 1
    新文本的預測標籤為: 0
    ```

<br>

___

_END_