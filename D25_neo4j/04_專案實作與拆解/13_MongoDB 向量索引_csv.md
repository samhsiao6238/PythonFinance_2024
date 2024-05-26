# 向量索引 `csv`

_使用 [yahoo! 財經](https://hk.finance.yahoo.com/quote/%5ETWII/history/) 資料_

<br>

## 步驟

1. 取得數據。
2. 處理數據：將數據轉換為適合的格式，例如 `CSV` 或 `JSON` 格式。
3. 轉換為向量：使用合適的嵌入技術將數據轉換為向量表示。
4. 存儲向量：將轉換為向量的數據存儲在 `MongoDB Atlas` 中。
5. 查詢數據：使用向量搜索技術進行語義查詢。



## 開始實作

1. 收集數據：`台股大盤1997_2024.csv.csv`。

2. 先查看資料內容。
```python
import pandas as pd
import streamlit as st

# 加載 CSV 文件
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Streamlit 介面
st.title("檢查 CSV 文件結構和內容")

# 加載數據
file_path = "台股大盤1997_2024.csv"
df = load_data(file_path)

# 顯示列名和前幾行數據
st.write("CSV 文件列名：")
st.write(df.columns.tolist())

st.write("CSV 文件前幾行數據：")
st.write(df.head())
```

## 建立向量儲存和查詢應用

1. 這段代碼從一個名為 `taiwan_stock_data.csv` 的文件中加載台股數據，將其轉換為向量表示並存儲到MongoDB Atlas中，其中使用 `TfidfVectorizer` 將文本數據轉換為向量，並以 Streamlit 建立網頁進行用戶互動，允許用戶輸入問題並觸發查詢。


2. `taiwan_stock_data.csv` 文件應包含描述性文本數據（例如每日收盤評論或每年市場報告）以便進行向量化處理。

3. `delete_existing_data` 函數會刪除集合中的所有文檔，確保在初始化新數據時不會超過空間配額，`perform_vector_search` 函數會根據輸入的查詢進行向量搜索，並返回最相似的前5個文檔。

4. 完整程式碼。。
```python

```