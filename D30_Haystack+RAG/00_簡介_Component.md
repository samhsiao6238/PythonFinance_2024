# 元件 `Component`

<br>

## 說明

1. 在 Haystack 和其他自然語言處理（NLP）框架中，`元件` 和 `模組` 有時會被混用，但它們的含義有所不同。

<br>

2. `元件` 是用於特定功能或操作的邏輯單元，通常用來執行特定任務或功能，在 `Haystack` 中，`元件` 代表各種處理步驟或功能單元，如文本嵌入、檢索、排序等。

<br>

## 特點

1. 功能專一：每個元件通常負責一個單一的功能。例如，`DocumentSplitter` 負責將文件分割成塊，`InMemoryBM25Retriever` 負責進行 BM25 檢索。

<br>

2. 可組合：元件可以通過管道（Pipeline）進行組合，以實現複雜的處理流程。例如，從文件儲存中檢索文件後，再通過嵌入模型進行查詢擴展。

<br>

3. 獨立性：元件之間相對獨立，可以靈活替換和重用。

<br>

## 常見的元件

1. 檢索器（Retriever）：`InMemoryBM25Retriever`，`InMemoryEmbeddingRetriever`

<br>

2. 嵌入器（Embedder）：`SentenceTransformersTextEmbedder`

<br>

3. 排序器（Ranker）：`TransformersSimilarityRanker`

<br>

4. 預處理器（Preprocessor）：`DocumentSplitter`

<br>

___

_END_