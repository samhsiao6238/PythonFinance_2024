# 元件 `Component`

_元件、組建 vs 模組_

<br>

## 說明

1. 在 `Haystack` 和其他 `自然語言處理（NLP）` 框架中，`元件、組件（Component）` 和 `模組（Module）` 有時可混用，但它們的含義是有所不同的。

<br>

2. 在 `Haystack` 中，`元件` 是用於特定功能或操作的 `邏輯單元`，通常用來執行特定任務或功能，如 `文本嵌入`、`檢索`、`排序` 等。

<br>

## 特點

1. 功能專一：每個 `元件` 通常負責一個單一功能，例如在後續的範例中，`DocumentSplitter` 負責將文件分割成塊，`InMemoryBM25Retriever` 負責進行 BM25 檢索等。

<br>

2. 可組合：元件可以通過 `管道（Pipeline）` 進行組合以實現複雜的處理流程，例如，從 `文件儲存` 中進行 `檢索文件` 後，再通過 `嵌入模型` 進行 `查詢擴展`。

<br>

3. 獨立性：元件雖可組合，但彼此間是獨立的，可以靈活更改和重用。

<br>

## 常見的元件

1. 檢索器（Retriever）：`InMemoryBM25Retriever`、`InMemoryEmbeddingRetriever`。

<br>

2. 嵌入器（Embedder）：`SentenceTransformersTextEmbedder`。

<br>

3. 排序器（Ranker）：`TransformersSimilarityRanker`。

<br>

4. 預處理器（Preprocessor）：`DocumentSplitter`。

<br>

___

_END_