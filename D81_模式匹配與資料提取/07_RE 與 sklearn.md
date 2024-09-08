# RE 與 sklearn


## 簡介

1. 前一部分主要側重於機器學習模型如 `spaCy` 輔助正則表達式進行資料提取，而範例特別針對文本中的命名實體識別（NER）應用。

2. 另外，結合 `sklearn` 與正則表達式的應用則是在文本分類領域特別適用，這個小節將著重於 `sklearn` 模組用於機器學習模型訓練與分類，例如文本分類，與 `命名實體識別` 有所不同。

## 常用場景

1. 文本分類任務：如垃圾郵件分類、情感分析等。

2. 篩選特定字詞：結合正則表達式對文本進行預處理（如移除雜訊、提取關鍵字），再使用 `sklearn` 的分類模型進行分析。

3. 在文本分類中，正則表達式可以作為資料清理與關鍵詞篩選的重要工具，而機器學習模型（如 `sklearn` 提供的 Naive Bayes、SVM 等）則擅長進行高階的文本分類任務。這種結合方式能有效地提升模型的性能，特別是在處理大量文本數據時。

## 範例

_使用 `sklearn` 進行文本分類，並結合正則表達式進行文本預處理_

1. 以下範例中，使用 `正則表達式` 處理文本的清理與篩選，如移除標點、數字、特定關鍵詞，另外使用 `sklearn` 處理文本分類，如將文本分為正向或負向情感類型。

```python
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# 模擬數據集，包含兩個分類：正向 (positive) 和負向 (negative)
data = {
    "text": [
        "I love this product! It is amazing.",
        "This is the worst experience I've ever had.",
        "Absolutely fantastic! Highly recommended.",
        "Not worth the price, very disappointed.",
        "Great quality and excellent customer service.",
        "Terrible product, broke after one use."
    ],
    "label": ["positive", "negative", "positive", "negative", "positive", "negative"]
}

# 將數據轉換為 pandas DataFrame
df = pd.DataFrame(data)

# 步驟 1：使用正則表達式清理文本
def clean_text(text):
    # 移除所有非字母的字元，保留字母和空格
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # 將文本轉換為小寫
    text = text.lower()
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

# 步驟 2：將文本轉換為特徵向量
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['cleaned_text'])

# 步驟 3：準備訓練和測試數據集
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 步驟 4：使用 Naive Bayes 進行文本分類
model = MultinomialNB()
model.fit(X_train, y_train)

# 步驟 5：進行預測並計算準確率
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"準確率: {accuracy * 100:.2f}%")
```


## 程式碼解釋

1. 其中 `clean_text()` 函數使用 `正則表達式` 移除所有 `非字母的字元`，如標點符號、數字等，並將所有字母轉換為小寫，這有助於文本的規範化處理；其中正則表達式模式 `r'[^a-zA-Z\s]'` 將匹配所有非字母的字元並將其移除。

2. 使用 `sklearn` 中的 `CountVectorizer` 將文本轉換為 `詞袋模型（Bag-of-Words）`，這是一種常見的 `文本特徵表示` 方法。

3. 使用 `Naive Bayes 模型 (MultinomialNB)` 進行文本分類。


## 應用場景擴展

1. 垃圾郵件過濾：正則表達式可以提前過濾常見的垃圾郵件特徵，如「免費」或「贏得獎品」等詞彙，並結合機器學習進行垃圾郵件分類。

2. 情感分析：結合特定情感詞的正則匹配（如「好」、「壞」、「喜歡」、「討厭」等）作為初步過濾，然後使用機器學習模型進行情感分類。

3. 網路評論分類：正則表達式可提取評論中的特定產品或服務名稱，再結合文本分類模型預測該評論的正負面情感。

