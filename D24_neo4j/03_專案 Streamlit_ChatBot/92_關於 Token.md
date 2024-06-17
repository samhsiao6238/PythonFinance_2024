# Token

<br>

## 說明

1. 在調用如 `GPT` 模型時，可透過設定 `max_tokens` 參數限制的是所產生的最大標記數，也就是控制產生文字的最大長度，如此便可確保產生的文字不會超過指定的長度，從而控制 API 呼叫的費用。

<br>

2. 具體範例。

    ```python
    import openai

    # 設定 API 金鑰
    openai.api_key = 'your-api-key'

    # 定義請求參數，包括 max_tokens
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a story about a brave knight."}
        ],
        # 設定最大產生的 token 數
        max_tokens=100,
    )

    # 輸出產生的回應
    print(response.choices[0].message['content'])
    ```

<br>

## 其他方法

_除了 `max_tokens`，還可以使用其他參數來最佳化和控制費用_

<br>

1. `temperature`: 控制生成文字的隨機性，較低的值會使產生的文字更確定性，較高的值會增加產生的多樣性。

<br>

2. `top_p`: 使用核採樣來控制生成文字的多樣性。

<br>

3. 範例。

    ```python
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a story about a brave knight."}
        ],
        # 設定最大產生的 token 數
        max_tokens=100,
        # 控制生成文字的隨機性
        temperature=0.7,
        # 使用核採樣來控制生成文字的多樣性
        top_p=0.9
    )
    ```

<br>

## 在本專案中應用

1. `llm` 是通過 `ChatOpenAI` 建立的物件，設置了 `max_tokens` 之後，任何調用 `llm` 之處都會遵循這個設置。

<br>

2. 具體使用。

    ```python
    import streamlit as st
    from langchain_openai import ChatOpenAI

    # 建立 ChatOpenAI 實體
    llm = ChatOpenAI(
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        model=st.secrets["OPENAI_MODEL"],
        # 設置最大 token
        max_tokens=100,
        # 設置隨機性
        temperature=0.7,
        # 核採樣
        top_p=0.9
    )

    from langchain_openai import OpenAIEmbeddings

    # OpenAIEmbeddings 是用來生成和處理嵌入向量（embeddings）
    # 這些嵌入向量是從使用 OpenAI 模型（如 GPT-4）生成的文本中取得的
    embeddings = OpenAIEmbeddings(
        openai_api_key=st.secrets["OPENAI_API_KEY"]
    )
    ```

___

_END_