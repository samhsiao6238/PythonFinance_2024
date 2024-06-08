# 使用 RAG 建立問答管道

_使用 PromptBuilder 和 OpenAIGenerator 來建立帶有檢索增強的生成問答管道。_

<br>

## 說明

1. 使用 Haystack 2.0 來創建使用檢索增強 (RAG) 方法的生成問答管道，包含以下主要模組及 `OpenAI API`。

    ```bash
    # 用於儲存和管理文檔
    InMemoryDocumentStore

    # 用於將文檔轉換為嵌入向量
    SentenceTransformersDocumentEmbedder
    
    # 將用戶的查詢轉換為嵌入向量
    SentenceTransformersTextEmbedder
    
    # 用於根據嵌入向量在內存中檢索相關文檔
    InMemoryEmbeddingRetriever
    
    # 用於創建模板提示
    PromptBuilder
    
    # 使用 OpenAI 的生成模型來生成文本的模組
    OpenAIGenerator  
    ```

<br>

2. 將使用 `七大奇蹟` 的維基百科頁面作為文件，也可替換為任何文本。

<br>

3. 安裝 Haystack 2.0 和其他所需的套件，並透過條件指定版本。

    ```bash
    pip install haystack-ai "datasets>=2.6.1" "sentence-transformers>=2.2.0"
    ```

<br>

## 範例說明

1. 索引文件：通過下載數據並將其嵌入索引到 `DocumentStore` 來創建問答系統，使用 `InMemoryDocumentStore` 來初始化 DocumentStore 以儲存問答系統用於查找答案的文件。

    ```python
    from haystack.document_stores.in_memory import InMemoryDocumentStore

    # 初始化內存文件儲存
    document_store = InMemoryDocumentStore()
    ```

<br>

2. 抓取數據：使用 `七大奇蹟` 的維基百科頁面作為文件，範例已經預處理數據並上傳到 Hugging Face Space：Seven Wonders，因此無需進行任何額外的清理或分割。

    ```python
    from datasets import load_dataset
    from haystack import Document

    # 加載數據集
    dataset = load_dataset(
        "bilgeyucel/seven-wonders", split="train"
    )
    docs = [
        Document(content=doc["content"],
        meta=doc["meta"]) for doc in dataset
    ]
    ```

<br>

3. 初始化文件嵌入器：要將數據儲存在帶有嵌入的 DocumentStore 中，使用模型名稱初始化一個 `SentenceTransformersDocumentEmbedder` 並調用 `warm_up()` 來下載嵌入模型。

    ```python
    from haystack.components.embedders import SentenceTransformersDocumentEmbedder

    # 初始化文件嵌入器
    doc_embedder = SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    doc_embedder.warm_up()
    ```

<br>

4. 運行後會顯示提示，表明這個擴充功能要求電腦必須安裝以下工具，而這些工具是不能透過擴充功能直接安裝的，如果下方有尚未安裝的工具，可點擊下面的連結進入下載頁面。

    ![](images/img_11.png)

<br>

5. 除此還包含了版本過舊的插件，其中已經安裝的會呈現反白，接著可分別點擊進行安裝，安裝了即便用不上也不影響 VSCode 運作，可放心安裝。

    ![](images/img_12.png)

<br>

6. 將文件寫入 DocumentStore：運行 `doc_embedder` 與文件，嵌入器將為每個文件創建嵌入並將這些嵌入儲存在文件對象的 `embedding` 字段中。然後使用 `write_documents()` 方法將文件寫入 DocumentStore。

    ```python
    # 創建文件嵌入並寫入文件儲存
    docs_with_embeddings = doc_embedder.run(docs)
    document_store.write_documents(docs_with_embeddings["documents"])
    ```

    ![](images/img_13.png)

<br>

5. 建立 RAG 管道：首先需要初始化文本嵌入器來為用戶查詢創建嵌入，創建的嵌入將由檢索器用來從 DocumentStore 中檢索相關文件。_請注意_，之前使用 `sentence-transformers/all-MiniLM-L6-v2` 模型創建了文件的嵌入，這裡需要使用相同的模型來嵌入用戶查詢。

    ```python
    from haystack.components.embedders import SentenceTransformersTextEmbedder

    # 初始化文本嵌入器
    text_embedder = SentenceTransformersTextEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    ```

<br>

6. 初始化檢索器：初始化一個 `InMemoryEmbeddingRetriever` 並讓其使用之前初始化的 `InMemoryDocumentStore`，這個檢索器將獲取與查詢相關的文件。

    ```python
    from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever

    # 初始化內存嵌入檢索器
    retriever = InMemoryEmbeddingRetriever(document_store)
    ```

<br>

7. 創建一個自定義提示，用於使用 RAG 方法進行生成問答任務。提示應該接受兩個參數：從文件儲存檢索到的文件和用戶的問題。使用 `Jinja2` 循環語法將檢索到的文件內容組合到提示中。接著使用提示模板初始化一個 `PromptBuilder` 實例。當給定必要的值時，`PromptBuilder` 將自動填充變量值並生成完整的提示。這種方法允許更具針對性和有效的問答體驗。

    ```python
    from haystack.components.builders import PromptBuilder

    # 定義模板提示
    template = """
    Given the following information, answer the question.

    Context:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    Question: {{question}}
    Answer:
    """

    # 初始化提示生成器
    prompt_builder = PromptBuilder(template=template)
    ```

<br>

8. 可將提示改為繁體中文。

    ```python
    from haystack.components.builders import PromptBuilder

    # 定義模板提示
    template = """
    根據以下信息，回答問題。

    上下文:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    問題: {{question}}
    答案:
    """

    # 初始化提示生成器
    prompt_builder = PromptBuilder(template=template)
    ```

<br>

9. 初始化生成器：生成器是與大型語言模型 (LLMs) 互動的模組，同時需要設置 `OPENAI_API_KEY` 環境變量，並初始化可與 OpenAI GPT 模型通信的 `OpenAIGenerator`。初始化時需指定模型名稱。

    ```python
    import os
    from getpass import getpass
    from haystack.components.generators import OpenAIGenerator

    # 設置 OpenAI API Key
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")

    # 初始化 OpenAI 生成器
    generator = OpenAIGenerator(model="gpt-4-turbo")
    ```

<br>

9. 建立管道：將所有模組添加到管道中並連接它們。將 `text_embedder` 的 `embedding` 輸出連接到 `retriever` 的 `query_embedding` 輸入，將 `retriever` 連接到 `prompt_builder`，並將 `prompt_builder` 連接到 `llm`。顯式連接 `retriever` 的輸出與 `prompt_builder` 的 `documents` 輸入，以使連接明顯，因為 `prompt_builder` 有兩個輸入（`documents` 和 `question`）。

    ```python
    from haystack import Pipeline

    # 初始化管道
    basic_rag_pipeline = Pipeline()

    # 添加模組到管道
    basic_rag_pipeline.add_component("text_embedder", text_embedder)
    basic_rag_pipeline.add_component("retriever", retriever)
    basic_rag_pipeline.add_component("prompt_builder", prompt_builder)
    basic_rag_pipeline.add_component("llm", generator)

    # 連接模組
    basic_rag_pipeline.connect(
        "text_embedder.embedding",
        "retriever.query_embedding"
    )
    basic_rag_pipeline.connect(
        "retriever",
        "prompt_builder.documents"
    )
    basic_rag_pipeline.connect(
        "prompt_builder",
        "llm"
    )
    ```

<br>

10. 輸出以下訊息，這裡逐行說明一下詳細內容。

    ```bash
    # 這是一個 Pipeline 對象，記憶體位置在 0x377e1a8c0，這位置不重要
    <haystack.core.pipeline.pipeline.Pipeline object at 0x377e1a8c0>
    # 組件
    🚅 Components
        # 嵌入器組件，使用 Sentence Transformers 模型將文本轉換成嵌入向量
        - text_embedder: SentenceTransformersTextEmbedder
        
        # 檢索器組件，從內存中根據嵌入向量檢索相關的文檔
        # 使用嵌入向量進行相似性檢索
        - retriever: InMemoryEmbeddingRetriever
        
        # 提示生成器，根據檢索到的文檔來構建提示 Prompt
        # 這些提示會被用來生成輸出或進行進一步的處理
        - prompt_builder: PromptBuilder
        
        # 大型語言模型生成器組件，使用 OpenAI 的生成器來生成自然語言文本回應
        - llm: OpenAIGenerator

    # 連接
    🛤️ Connections
        # 組件將文本轉換為嵌入向量（embedding）
        # 這些嵌入向量作為 retriever 組件的輸入查詢嵌入（query_embedding）
        - text_embedder.embedding -> retriever.query_embedding (List[float])
        
        # 組件根據查詢嵌入檢索到的相關文檔（documents）
        # 這些文檔被傳遞給 prompt_builder 組件
        - retriever.documents -> prompt_builder.documents (List[Document])
        
        # 組件根據文檔生成一個提示（prompt）
        # 這個提示被傳遞給 llm 組件來生成最終的自然語言回應
        - prompt_builder.prompt -> llm.prompt (str)
    ```

<br>

11. 使用管道的 `run()` 方法進行提問，在 `text_embedder` 和 `prompt_builder` 參數中會依據模板提示中的 `question` 變量進行提問。

    ```python
    # 提問
    '''
    Rhodes 雕像是什麼樣子的？
    巴比倫花園在哪裡？
    人們為什麼要建造吉薩大金字塔？
    人們為什麼參觀阿耳忒彌斯神殿？
    羅德島巨像的重要性是什麼？
    摩索拉斯墓發生了什麼事？
    羅德島巨像是怎麼崩潰的？
    '''
    question = "人們為什麼參觀阿耳忒彌斯神殿？"

    response = basic_rag_pipeline.run({
        "text_embedder": {"text": question},
        "prompt_builder": {"question": question}
    })

    # 輸出答案
    print(response["llm"]["replies"][0])
    ```

    _Rhodes 雕像是什麼樣子的？答案：_

    Rhodes 雕像，也稱為羅得島的太陽神赫利俄斯巨像（Colossus of Rhodes），是一座代表希臘太陽神赫利俄斯的巨大青銅雕像。根據當時的描述，這座雕像高約70肘，即大約33米（108英尺），這使它成為古代世界中最高的雕像之一，大約與現代自由女神像從腳到頭冠的高度相當。雕像由鐵條組成的內架和銅板形成的表皮構成，內部填充石塊，支撐著整座雕像的結構。雕像本身約位於羅得島港口入口附近的一個15米高的白色大理石基座上。雕像的頭部有著标准化的面貌，特點包括卷曲的頭髮和均匀分布的金屬火焰狀尖刺，這些特徵與當時羅得島的硬幣上的圖像相似。

    _人們為什麼參觀阿耳忒彌斯神殿？答案：_
    
    人們參觀阿耳忒彌斯神殿的原因多樣。首先，這座神殿是一個重要的宗教地標，供奉著女神阿耳忒彌斯，吸引了許多虔誠的朝聖者前來參拜和獻祭。其次，神殿本身的建築和藝術價值也吸引了不少遊客和學者，例如神殿的豐富細節和精緻雕刻。此外，神殿還提供了庇護，對於逃避迫害或懲罰的人來說是一個避難所，這項功能也使得許多尋求保護的人士前來。最後，許多商人、國王和觀光客也會造訪此地，他們可能是出於對神殿的好奇或者文化旅遊的目的。因此，阿耳忒彌斯神殿成為了一個結合宗教、文化和歷史的多功能景點。


<br>

___

_END_