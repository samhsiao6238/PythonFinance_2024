# 建立 LLM

## 說明

1. 建立資料夾 `.streamlit`。

2. 使用 `st.secrets.toml` 來儲存敏感資訊。
```toml
OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXX"
OPENAI_MODEL = "gpt-4-turbo"
```

3. 建立資料夾 `solutions`，建立檔案 `llm.py`。
```python
# llm.py
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# 取得環境變數
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_MODEL = st.secrets["OPENAI_MODEL"]

# 建立 ChatOpenAI 實體
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
)

# OpenAIEmbeddings 是用來生成和處理嵌入向量（embeddings）
# 這些嵌入向量是從使用 OpenAI 模型（如 GPT-4）生成的文本中獲取的
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
```