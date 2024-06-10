# 使用 Multiplexer 簡化管道輸入

![](images/img_69.png)

## 說明

1. 這是官方在 `2024/05/10` 發佈的 [官方教程](https://haystack.deepset.ai/tutorials/37_simplifying_pipeline_inputs_with_multiplexer)，另外需要搭配 `Hugging Face API Key` 使用，整體目標是使用 Multiplexer 簡化 `RAG 管道` 中的 `Pipeline.run()` 的輸入。

2. 在構建超過 3 或 4 個組件的 Haystack 管道時，可注意到傳遞給 `Pipeline.run()` 方法的輸入數量會無限增長，新的組件會從管道中的其他組件接收一些輸入，但許多組件也需要來自用戶的額外輸入，因此 `Pipeline.run()` 的數據輸入會變得非常重複，這個狀況可透過 `Multiplexer` 有效地管理這些重複。

## 使用的組件

1. `Multiplexer`：

2. `InMemoryDocumentStore`：

3. `HuggingFaceAPIDocumentEmbedder`：

4. `HuggingFaceAPITextEmbedder`：

5. `InMemoryEmbeddingRetriever`：

6. `PromptBuilder`：

7. `HuggingFaceAPIGenerator`：

8. `AnswerBuilder`：


## 開始

1. 安裝依賴庫。

```bash
pip install haystack-ai "huggingface_hub>=0.22.0"
```

2. 設置 `Hugging Face API Key`。

```python
from getpass import getpass
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["HF_API_TOKEN"] = os.getenv("HF_API_TOKEN")

if "HF_API_TOKEN" not in os.environ:
    os.environ["HF_API_TOKEN"] = getpass("Enter Hugging Face token:")
```

## 使用管道索引文件

1. 導入組件。
```python
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import HuggingFaceAPIDocumentEmbedder
```


2. 模組小型的數據集。
```python
# 建立文件數據集
documents = [
    Document(content="My name is Jean and I live in Paris."),
    Document(content="My name is Mark and I live in Berlin."),
    Document(content="My name is Giorgio and I live in Rome."),
    Document(content="My name is Giorgio and I live in Milan."),
    Document(content="My name is Giorgio and I lived in many cities, but I settled in Naples eventually."),
]
```

3. 創建索引管道並添加組件。
```python
# 創建索引管道
indexing_pipeline = Pipeline()

# 添加組件
# 使用 `HuggingFaceAPIDocumentEmbedder` 為文件 `生成嵌入`
indexing_pipeline.add_component(
    instance=HuggingFaceAPIDocumentEmbedder(
        api_type="serverless_inference_api",
        api_params={
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        }
    ),
    name="doc_embedder"
)
```

4. 建立文件儲存對象 `InMemoryDocumentStore`，將範例數據集儲存在這個內存文件儲存並生成嵌入。

```python
# 初始化內存文件儲存
document_store = InMemoryDocumentStore()
```

5. 並通過 `DocumentWriter` 將它們寫入 `文件儲存(document store)`。
```python
# 添加 DocumentWriter 組件，用於將生成的嵌入寫入內存文件儲存
indexing_pipeline.add_component(
    instance=DocumentWriter(document_store=document_store),
    name="doc_writer"
)
```

6. 將添加到管道的組件進行連接，然後運行管道。
```python
# 連接組件
indexing_pipeline.connect(
    "doc_embedder.documents", "doc_writer.documents"
)

# 運行索引管道
indexing_pipeline.run(
    {"doc_embedder": {"documents": documents}}
)
```

## 構建 RAG 管道

1. 導入構建 `RAG 管道` 的組件。

```python
from haystack.components.embedders import HuggingFaceAPITextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder, AnswerBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
```


2. 建立模板。

```python
# 定義模板
template = """
<|user|>
根據給定的上下文回答問題。

上下文：
{% for document in documents %}
    {{ document.content }}
{% endfor %}

問題：{{ question }}</s>

<|assistant|>
答案：
"""
```

3. 建立管道。
```python
# 創建管道
pipe = Pipeline()
```

4. 添加組件：生成器、檢索器、HuggingFaceAPI 生成器。
```python
# 添加嵌入生成器
pipe.add_component(
    "embedder",
    HuggingFaceAPITextEmbedder(
        api_type="serverless_inference_api", api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"}
    ),
)

# 添加內存嵌入檢索器
pipe.add_component(
    "retriever",
    InMemoryEmbeddingRetriever(document_store=document_store)
)

# 添加模板生成器
pipe.add_component(
    "prompt_builder",
    PromptBuilder(template=template)
)

# 添加 HuggingFaceAPIGenerator 組件，用於生成答案
pipe.add_component(
    "llm",
    HuggingFaceAPIGenerator(
        api_type="serverless_inference_api",
        api_params={"model": "HuggingFaceH4/zephyr-7b-beta"}
    )
)

# 添加答案構建器
pipe.add_component(
    "answer_builder",
    AnswerBuilder()
)
```

5. 連接組件。
```python
# 連接組件
pipe.connect("embedder.embedding", "retriever.query_embedding")
pipe.connect("retriever", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")
pipe.connect("llm.replies", "answer_builder.replies")
pipe.connect("llm.meta", "answer_builder.meta")
```

---

## 運行管道

將查詢傳遞給 `embedder`、`prompt_builder` 和 `answer_builder` 並運行它：

```python
query = "Where does Mark live?"
pipe.run({"embedder": {"text": query}, "prompt_builder": {"question": query}, "answer_builder": {"query": query}})
```

在這個基本的 RAG 管道中，需要查詢來操作的組件有 `embedder`、`prompt_builder` 和 `answer_builder`。但是，隨著管道的擴展，新增的組件如檢索器和排名器也可能需要查詢，這會導致 `Pipeline.run()` 調用變得非常重複且日益複雜。在這種情況下，使用 Multiplexer 可以幫助簡化和減少 `Pipeline.run()` 的複雜度。

---

## 介紹 Multiplexer

Multiplexer 是一個可以接受多個輸入連接，並將其接收到的第一個值分發給所有連接到其輸出的組件。在這種設置中，您可以通過將其連接到需要在運行時接收查詢的其他管道組件來使用這個組件。

現在，用期望的輸入類型（在這種情況下是 `str`，因為查詢是一個字符串）初始化 Multiplexer：

```python
from haystack.components.others import Multiplexer

# 初始化 Multiplexer，指定輸入類型為字符串
multiplexer = Multiplexer(str)
```

---

## 將 Multiplexer 添加到管道

創建相同的 RAG 管道，但這次加入 Multiplexer。將 Multiplexer 添加到管道並連接到所有需要查詢作為輸入的組件：

```python
from haystack.components.embedders import HuggingFaceAPITextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbedding

Retriever
from haystack.components.builders import PromptBuilder, AnswerBuilder
from haystack.components.generators import HuggingFaceAPIGenerator

template = """
 
 Answer the question based on the given context.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}
Question: {{ question }}</s>

Answer:
"""

# 創建管道
pipe = Pipeline()

# 添加 Multiplexer 組件
pipe.add_component("multiplexer", multiplexer)

# 添加嵌入生成器
pipe.add_component(
    "embedder",
    HuggingFaceAPITextEmbedder(
        api_type="serverless_inference_api", api_params={"model": "sentence-transformers/all-MiniLM-L6-v2"}
    ),
)

# 添加內存嵌入檢索器
pipe.add_component("retriever", InMemoryEmbeddingRetriever(document_store=document_store))

# 添加模板生成器
pipe.add_component("prompt_builder", PromptBuilder(template=template))

# 添加 HuggingFaceAPIGenerator 組件，用於生成答案
pipe.add_component(
    "llm",
    HuggingFaceAPIGenerator(api_type="serverless_inference_api", api_params={"model": "HuggingFaceH4/zephyr-7b-beta"}),
)

# 添加答案構建器
pipe.add_component("answer_builder", AnswerBuilder())

# 將 Multiplexer 連接到所有需要查詢的組件
pipe.connect("multiplexer.value", "embedder.text")
pipe.connect("multiplexer.value", "prompt_builder.question")
pipe.connect("multiplexer.value", "answer_builder.query")

# 連接其餘組件
pipe.connect("embedder.embedding", "retriever.query_embedding")
pipe.connect("retriever", "prompt_builder.documents")
pipe.connect("prompt_builder", "llm")
pipe.connect("llm.replies", "answer_builder.replies")
pipe.connect("llm.meta", "answer_builder.meta")
```

---

## 使用 Multiplexer 運行管道

運行更新後的管道，這次您只需將查詢傳遞給 Multiplexer，而不是單獨傳遞給 `prompt_builder`、`retriever` 和 `answer_builder`，結果會相同。

```python
pipe.run({"multiplexer": {"value": "Where does Mark live?"}})
```

---

## 下一步

🎉 恭喜！您已經學會如何使用 Multiplexer 簡化管道運行！

如果您喜歡這個教程，還有更多關於 Haystack 2.0 的知識等著您學習：

- 創建混合檢索管道
- 使用條件路由構建後備方案進行 Web 檢索
- 基於模型的 RAG 管道評估

若想了解最新的 Haystack 動態，您可以訂閱我們的新聞簡報或加入 Haystack Discord 社區。

感謝閱讀！