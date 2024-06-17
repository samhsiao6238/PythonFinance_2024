# 建立連結

_利用 Amazon Bedrock 和 LangChain 的 Streamlit 應用程式_

_我個人覺得這個專案很雞肋，用來參考可以，實用性、可用性極低。_

<br>

## 說明

1. 這個範例可透過輸入某人姓名後搜尋其在 LinkedIn 個人資料，然後提供有關該人的簡潔摘要。

2. 程序是透過 `Amazon Bedrock` 進行深入研究數據並得出有意義的見解。

3. 另外使用 LangChain 作為語言處理，使得程式可以從 LinkedIn 詳細資訊中得出清晰的摘要。

<br>

## 取得 Proxycurl API Key

_Proxycurl 是一個專門用於取得 LinkedIn 資料的 API_

<br>

1. 進入 [Proxycurl 註冊頁面](https://nubela.co/proxycurl/#/signup) 並建立一個新帳戶。

    ![](images/img_01.png)

<br>

2. 可選擇 Google 帳號。

    ![](images/img_02.png)

<br>

3. 進入後可取得 API Key。

    ![](images/img_03.png)

<br>

## 取得 SerpAPI API Key

_SerpAPI 是一個搜索引擎結果頁面 (SERP) 的 API_

<br>

1. 訪問 [SerpAPI 註冊頁面](https://serpapi.com/users/sign_up) 並建立一個新帳戶。

    ![](images/img_04.png)

<br>

2. 進入就會看到 API Key。

    ![](images/img_05.png)

<br>

## 步驟

1. 要在 `.env` 中寫入 Proxycurl and Serpa API Key。

    ```bash
    PROXYCURL_API_KEY=<YOUR API KEY>
    SERPAPI_API_KEY=<YOUR API KEY>
    ```

<br>

2. 將前面步驟取得的兩個密鑰都寫入 `.env`

    ![](images/img_06.png)

<br>

3. 安裝腳本所需套件。

    ```bash
    pip install -r requirements.txt
    ```

<br>

4. 啟動服務。

    ```bash
    streamlit run app.py
    ```

<br>

## 排除錯誤

1. 正在使用的 LangChain 庫中的一些類和方法已被棄用。

<br>

2. LinkedIn 搜尋代理沒有有效的工具來抓取 LinkedIn 資料。

<br>

## 更新 LangChain 的導入和使用

1. `Bedrock` 應從 `langchain_community.llms` 導入，而 `LLMChain` 應該使用 `RunnableSequence`。

<br>

2. 需要確保 `lookup` 函數和 `scrape_linkedin_profile` 函數正確工作並返回有效的 LinkedIn URL 和資料。

<br>

## 完整腳本

_修改後的_

<br>

1. 專案結構。

    ```bash
    .
    ├── agents
    │   └── linkedin_lookup_agent.py
    ├── app.py
    ├── requirements.txt
    ├── third_parties
    │   └── linkedin.py
    └── tools
        └── tools.py
    ```

2. app.py
```python

```

3. linkedin_lookup_agent.py
```python

```
4. linkedin.py
```python

```
5. tools.py
```python

```

