# Haystack

_[Haystack 官網](https://haystack.deepset.ai/)、[deepset 官網](https://www.deepset.ai/) 與 [Haystack GitHub](https://github.com/deepset-ai/haystack)_

_由於 2.0 與 1.x 有相容性問題，所以參考教程的時候特別注意版本，這裡將使用 [2.0 教程](https://haystack.deepset.ai/tutorials)_

<br>

## 簡介

1. `Haystack` 是由 `deepset GmbH` 開發的開源框架，而 `deepset` 成立於 2018 年，是一家專注於建立和推動自然語言處理（NLP）技術的公司，主要產品有 `Haystack`、`deepset Cloud`，其中 `Haystack` 是一個在開源社區很受歡迎的 NLP 工具。

<br>

2. `Haystack` 用於建立基於 `搜索` 和 `問答` 的應用程序，允許開發者建立和部署 `端到端` 的自然語言處理（NLP）管道，特別適合處理大型文件集合，並在這些文件中找到準確答案。

<br>

3. `Haystack` 支持多種 NLP 模型和數據儲存，並且能夠與各種檢索後端無縫集成，如 Elasticsearch、FAISS、Milvus 等。

<br>

## 主要功能

1. 文件檢索 (Document Retrieval)。

   - 使用向量搜索和 `BM25` 這樣的傳統方法進行高效的文件檢索。

   - 支持多種 `向量搜索引擎`，如 `Elasticsearch`、`FAISS` 和 `Milvus`。

<br>

2. 問答系統 (Question Answering)。

   - 支持基於 transformer 模型的問答系統，如 BERT、RoBERTa 和其他 Hugging Face 模型。

   - 支持使用 Retriever-Reader 架構，其中檢索器 (Retriever) 負責找到相關文件，而閱讀器 (Reader) 負責從文件中提取答案。

<br>

3. 生成回答 (Answer Generation)。

   - 使用生成模型（如 GPT-4-turbo）來生成更加自然的回答。

<br>

4. 管道組裝 (Pipeline Assembly)。

   - 使用靈活的管道架構，可以組裝和配置不同的模組以滿足具體需求。

   - 支持自定義模組和流程，以滿足複雜的業務需求。

<br>

5. 多語言支持。

   - 支持多語言文件處理和查詢。

<br>

## 優勢

1. 開源和靈活性。

   - 作為開源框架，Haystack 提供了高度的靈活性和可擴展性，可以根據需求進行定制。

<br>

2. 端到端的解決方案。

   - Haystack 提供了從文件檢索到答案生成的完整解決方案，適合建立各種信息檢索和問答系統。

<br>

3. 社區支持和文件。

   - 擁有活躍的開發者社區和詳細的文件，使得上手和使用更加簡單。

<br>

## 類似框架

_其他解決自然語言處理和問答系統的框架或服務_

<br>

_AWS (Amazon Web Services)_

1. Amazon Comprehend

   - 一個完全託管的自然語言處理服務，可以自動提取文本中的見解和關係，包括情感分析、實體識別、關鍵短語提取和語言檢測。

   - 提供 API 來建立和部署 NLP 應用，適合處理大量文本數據。

<br>

2. Amazon Kendra

   - 一個高效的企業搜索服務，利用機器學習來提供準確且相關的搜索結果。

   - 支持文件檢索和問答功能，類似於 Haystack 的檢索和閱讀器架構。

<br>

_Google Cloud_

1. Dialogflow

   - 一個建立聊天機器人和語音應用的開發套件，適合建立多種對話應用，包括客服機器人、互動代理等。

   - 支持多語言，並且可以集成到各種平台，如 Google Assistant、Messenger 和 Slack。

<br>

2. Cloud Natural Language API

   - 提供文本分析功能，包括情感分析、實體識別、語法分析和文本分類。

   - 可以與 Google 的其他服務（如 BigQuery）集成，用於更大規模的數據分析。

<br>

3. Google Cloud Search

   - 一個企業搜索解決方案，利用 Google 的搜索技術來提供高效的內部文件和數據檢索服務。

<br>

_OpenAI_

1. OpenAI GPT

   - 一個強大的生成模型，可以用於多種 NLP 任務，包括文本生成、翻譯、摘要、問答等。

   - 通過 API 提供服務，可以用於建立智能的對話系統和問答系統。

<br>

_Microsoft Azure_

1. Azure Cognitive Services

   - 提供一系列 NLP 和語音服務，包括文本分析、語音識別、翻譯和聊天機器人建立工具。

   - Azure 的文本分析服務支持情感分析、實體識別、關鍵短語提取等功能。

<br>

2. Azure Search

   - 一個完全託管的搜索服務，支持全文搜索、過濾、排序和自動補全功能。

   - 可以用於建立基於搜索的應用，包括企業搜索和問答系統。

<br>

_IBM Watson_

1. Watson Discovery

   - 一個智能搜索和內容分析平台，利用 AI 技術來發現和分析大量非結構化數據。

   - 支持文件檢索和問答功能，類似於 Haystack 的檢索和閱讀器架構。

<br>

2. Watson Assistant

   - 一個建立對話機器人的平台，支持多種語言和多渠道的集成。

   - 提供自然語言理解和對話管理功能，適合建立智能的客服系統。

<br>

___

_END_