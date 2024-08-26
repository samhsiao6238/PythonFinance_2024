# LlamaIndex

_以前稱為 GPT Index_

<br>

## 說明

1. 這是一個開源的數據框架，用於幫助開發者將大型語言模型如 OpenAI 的 GPT、Meta 的 LLaMA 等與各種數據源進行集成。

<br>

2. LlamaIndex 旨在簡化從不同數據來源如文件、API、資料庫等提取和處理數據，並將其有效地輸入到大型語言模型中，使這些模型能夠更好地理解和生成相關的自然語言輸出。

<br>

## 主要功能

1. LlamaIndex 提供了一系列工具和接口，可讓開發者將不同類型的數據如結構化和非結構化數據整合到一個統一的索引中，這些數據來源可以包括 PDF 文件、網頁、資料庫記錄、API 響應等。

<br>

2. LlamaIndex 提供了多種索引結構選項如樹狀索引、列表索引、向量索引等，可根據具體的應用場景選擇最合適的索引方式，從而提高數據查詢和檢索的效率。

<br>

3. LlamaIndex 能夠處理用戶查詢並利用索引進行高效檢索，結合大型語言模型的生成能力，生成上下文相關的自然語言響應。

<br>

4. LlamaIndex 提供了接口和工具，允許開發者使用流行的 LLMs，如 GPT-3、GPT-4、LLaMA、Claude 等來處理數據和生成文本，這些接口可以讓模型根據索引數據生成更具上下文和更精確的回答。

<br>

## 在 Python 中的應用範例

_以下是如何使用 LlamaIndex 與 OpenAI 的 GPT 模型集成進行查詢的一個基本範例_

<br>

1. 使用以下命令安裝 LlamaIndex 和 OpenAI 的 Python 庫。

    ```bash
    pip install llama-index openai
    ```

<br>

2. 假設有一些文本文檔，想使用 LlamaIndex 來構建索引並進行查詢。

    ```python
    from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor
    from llama_index import ServiceContext
    from langchain.chat_models import ChatOpenAI

    # 設定 OpenAI API 金鑰
    openai_api_key = "Open API 密鑰"

    # 從指定資料夾中讀取文件並加載數據
    documents = SimpleDirectoryReader('文件路徑').load_data()

    # 設置並使用 GPT 模型作為預測器，將其整合到 LlamaIndex 中
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(
            temperature=0.5, 
            model_name="gpt-3.5-turbo", 
            openai_api_key=openai_api_key
        )
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor
    )

    # 使用向量化索引來構建數據索引
    # 這樣的索引更適合用於自然語言查詢
    index = GPTVectorStoreIndex.from_documents(
        documents, 
        service_context=service_context
    )

    # 通過該引擎來處理查詢並生成對應的自然語言響應
    query_engine = index.as_query_engine()

    # 執行查詢
    response = query_engine.query(
        "What is the main topic of the documents?"
    )
    print(response)
    ```

<br>

___

_END_
