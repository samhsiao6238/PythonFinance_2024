# Chat App

![](images/img_35.png)

<br>

## 說明

1. 這是官方在 `2024/04/25` 發布的 [官方教程](https://haystack.deepset.ai/tutorials/40_building_chat_application_with_function_calling)，構建一個具有 `函數調用` 功能的 `聊天應用程序` 。

<br>

2. 使用到的組件包含 `InMemoryDocumentStore`、`SentenceTransformersDocumentEmbedder`、`SentenceTransformersTextEmbedder`、`InMemoryEmbeddingRetriever`、`PromptBuilder`、`OpenAIGenerator`、`OpenAIChatGenerator`，另外也會使用 `OpenAI API`。

<br>

3. 這個範例的目的是使用 `OpenAI` 的 `函數調用功能 `來構建具備 `類代理行為` 的聊天應用程序，將 Haystack 管道轉換為函數調用工具，以及使用 OpenAI 的 Chat Completion API 通過 OpenAIChatGenerator 來實現類代理行為的應用程序。相關文件可參考 Haystack 的 [OpenAIChatGenerator 文件](https://docs.haystack.deepset.ai/docs/openaichatgenerator)。

<br>

4. OpenAI 的 `函數調用功能` 將 `LLM` 連接到外部工具，通過向 `OpenAI API` 調用提供函數列表及其規範可輕鬆構建聊天助手，這些助手可以通過調用外部 API 來回答問題或從文本中提取結構化信息。

<br>

## 進行開發

1. 安裝 Haystack 2.0 和 `sentence-transformers`。

    ```bash
    pip install haystack-ai "sentence-transformers>=2.2.0"
    ```

<br>

2. 保存 OpenAI API Key 為環境變量。

    ```python
    from getpass import getpass
    import os
    from dotenv import load_dotenv

    # 載入環境變數
    load_dotenv()
    # 兩個 API 的密鑰
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")
    ```

<br>

## OpenAIChatGenerator vs OpenAIGenerator

1. `OpenAIChatGenerator` 是支持通過 `Chat Completion API` 使用 `OpenAI` 的函數調用功能的組件，與 `OpenAIGenerator` 不同，`OpenAIChatGenerator` 是通過 `ChatMessage` 列表來進行通信的。

<br>

2. 實作上，使用 `ChatMessage.from_system()` 創建一個具有 `SYSTEM` 角色的 `ChatMessage` 對象，然後使用 `ChatMessage.from_user()` 創建另一個具有 `USER` 角色的 `ChatMessage`。接著，將這些消息列表傳遞給 `OpenAIChatGenerator` 並運行。

    ```python
    from haystack.dataclasses import ChatMessage
    from haystack.components.generators.chat import OpenAIChatGenerator

    # 創建系統消息和用戶消息的 ChatMessage 對象
    messages = [
        ChatMessage.from_system(
            "即使某些輸入資料採用其他語言，也始終以繁體中文回應。"
        ),
        ChatMessage.from_user(
            "什麼是自然語言處理？要簡潔。"
        ),
    ]

    # 初始化 OpenAIChatGenerator
    chat_generator = OpenAIChatGenerator(model="gpt-4-turbo")
    # 傳入消息並運行
    chat_generator.run(messages=messages)
    ```

<br>

3. 輸出如下結果。

    ```python
    {
        "replies": [
            ChatMessage(
                content="自然語言處理（NLP）是人工智能的一個分支，它使計算機能夠理解、解釋和生成人類語言。主要應用包括語音識別、語言翻譯和情感分析。",
                role=<ChatRole.ASSISTANT: "assistant">,
                name=None,
                meta={
                    "model": "gpt-4-turbo-2024-04-09",
                    "index": 0,
                    "finish_reason": "stop",
                    "usage": {
                        "completion_tokens": 82,
                        "prompt_tokens": 67,
                        "total_tokens": 149
                    }
                }
            )
        ]
    }
    ```

<br>

## 基本流式處理

1. `OpenAIChatGenerator` 支持流式處理，以下提供一個 `streaming_callback` 函數並重新運行 `chat_generator` 來查看差異。

    ```python
    from haystack.dataclasses import ChatMessage
    from haystack.components.generators.chat import OpenAIChatGenerator
    from haystack.components.generators.utils import print_streaming_chunk

    # 使用流式回調函數初始化 OpenAIChatGenerator
    chat_generator = OpenAIChatGenerator(
        model="gpt-4-turbo",
        streaming_callback=print_streaming_chunk
    )
    # 傳入消息並運行
    response = chat_generator.run(messages=messages)
    ```

<br>

## 從 Haystack 管道創建函數調用工具

1. 要使用 `OpenAI` 的 `函數調用功能`，需要通過 `generation_kwargs` 參數將工具介紹給 `OpenAIChatGenerator`，本範例使用 `Haystack RAG` 管道作為工具之一，因此需要將文件索引到文件儲存中，然後在其上構建 RAG 管道。

<br>

2. 創建一個管道，將範例數據集儲存到 `InMemoryDocumentStore` 中，並使用 `SentenceTransformersDocumentEmbedder` 來生成文件的嵌入，然後使用 `DocumentWriter` 將它們寫入 `文件儲存`中，將這些組件添加到管道後，將它們連接並運行管道。

    ```python
    from haystack import Pipeline, Document
    from haystack.document_stores.in_memory import InMemoryDocumentStore
    from haystack.components.writers import DocumentWriter
    from haystack.components.embedders import SentenceTransformersDocumentEmbedder

    # 創建文件
    documents = [
        Document(content="我的名字是 Jean，我住在 Paris。"),
        Document(content="我的名字是 Mark，我住在 Berlin。"),
        Document(content="我的名字是 Giorgio，我住在 Rome。"),
        Document(content="我的名字是 Marta，我住在 Madrid。"),
        Document(content="我的名字是 Harry，我住在 London。"),
    ]

    # 初始化內存文件儲存
    document_store = InMemoryDocumentStore()

    # 創建索引管道
    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component(
        instance=SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2"), name="doc_embedder"
    )
    indexing_pipeline.add_component(
        instance=DocumentWriter(document_store=document_store),
        name="doc_writer"
    )

    # 連接嵌入器和文件寫入器
    indexing_pipeline.connect(
        "doc_embedder.documents",
        "doc_writer.documents"
    )

    # 運行管道
    indexing_pipeline.run({
        "doc_embedder": {"documents": documents}
    })
    ```

<br>

3. 運行後顯示。

    ![](images/img_36.png)

<br>

## 構建 RAG 管道

1. 使用 `SentenceTransformersTextEmbedder`、`InMemoryEmbeddingRetriever`、`PromptBuilder` 和 `OpenAIGenerator` 構建基本的檢索增強生成管道。

    ```python
    from haystack.components.embedders import SentenceTransformersTextEmbedder
    from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
    from haystack.components.builders import PromptBuilder
    from haystack.components.generators import OpenAIGenerator

    # 定義提示模板
    template = """
    根據給定的上下文回答問題。

    上下文:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}
    問題: {{ question }}
    答案:
    """

    # 創建 RAG 管道
    rag_pipe = Pipeline()
    rag_pipe.add_component(
        "embedder",
        SentenceTransformersTextEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
    )
    rag_pipe.add_component(
        "retriever",
        InMemoryEmbeddingRetriever(
            document_store=document_store
        )
    )
    rag_pipe.add_component(
        "prompt_builder",
        PromptBuilder(
            template=template
        )
    )
    rag_pipe.add_component(
        "llm",
        OpenAIGenerator(model="gpt-4-turbo")
    )

    # 連接組件
    rag_pipe.connect(
        "embedder.embedding",
        "retriever.query_embedding"
    )
    rag_pipe.connect(
        "retriever",
        "prompt_builder.documents"
    )
    rag_pipe.connect(
        "prompt_builder",
        "llm"
    )
    ```

<br>

2. 會輸出以下訊息。

    ```bash
    <haystack.core.pipeline.pipeline.Pipeline object at 0x3169ca710>

    🚅 Components
        - embedder: SentenceTransformersTextEmbedder
        - retriever: InMemoryEmbeddingRetriever
        - prompt_builder: PromptBuilder
        - llm: OpenAIGenerator

    🛤️ Connections
        - embedder.embedding -> retriever.query_embedding (List[float])
        - retriever.documents -> prompt_builder.documents (List[Document])
        - prompt_builder.prompt -> llm.prompt (str)
    ```

<br>

## 運行管道

1. 使用一個查詢來測試管道，並確保它按照預期工作，然後再將其用作函數調用工具。

    ```python
    query = "Mark 住在哪裡？"
    rag_pipe.run({
        "embedder": {"text": query},
        "prompt_builder": {"question": query}
    })
    ```

<br>

2. 會顯示以下結果。

    ![](images/img_37.png)

<br>

## 將 Haystack 管道轉換為工具

1. 將 `rag_pipe.run` 調用包裝成一個函數 `rag_pipeline_func`，這個 `rag_pipeline_func` 函數將接受一個查詢並返回來自 RAG 管道的 LLM 的回應，然後可將此函數作為工具引入到 `OpenAIChatGenerator` 中。

    ```python
    def rag_pipeline_func(query: str):
        result = rag_pipe.run({
            "embedder": {"text": query},
            "prompt_builder": {"question": query}
        })
        return {"reply": result["llm"]["replies"][0]}
    ```

<br>

## 創建工具列表

1. 除了 `rag_pipeline_func` 工具外，還創建一個名為 `get_current_weather` 的新工具，用於獲取 `城市的天氣信息`，以下函數中使用硬編碼的數據來展示功能。

    ```python
    WEATHER_INFO = {
        "Berlin": {
            "weather": "mostly sunny", "temperature": 7, "unit": "celsius"
        },
        "Paris": {
            "weather": "mostly cloudy", "temperature": 8, "unit": "celsius"
        },
        "Rome": {
            "weather": "sunny", "temperature": 14, "unit": "celsius"
        },
        "Madrid": {
            "weather": "sunny", "temperature": 10, "unit": "celsius"
        },
        "London": {
            "weather": "cloudy", "temperature": 9, "unit": "celsius"
        },
    }

    def get_current_weather(location: str):
        if location in WEATHER_INFO:
            return WEATHER_INFO[location]
        else:
            # 回退數據
            return {
                "weather": "sunny",
                "temperature": 21.8,
                "unit": "fahrenheit"
            }
    ```

<br>

2. 接下來，按照 `OpenAI` 的工具架構為 `rag_pipeline_func` 和 `get_current_weather` 添加函數說明。詳細說明 `rag_pipeline_func` 和 `query`，以便 OpenAI 可以生成適當的參數。

    ```python
    tools = [
        {
            "type": "function",
            "function": {
                "name": "rag_pipeline_func",
                "description": "獲取有關人們居住地點的信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜尋中使用的查詢。從用戶的消息中推斷出這一點。它應該是一個問題或一個陳述。",
                        }
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "取得當前天氣",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市和州，例如加州舊金山"
                        }
                    },
                    "required": ["location"],
                },
            },
        },
    ]
    ```

<br>

## 使用工具運行 OpenAIChatGenerator

1. 要使用函數調用功能，您需要在 `OpenAIChatGenerator` 的 `run()` 方法中傳入工具列表作為 `generation_kwargs`。用系統消息指導模型使用提供的工具，然後作為用戶消息提供一個需要函數調用的查詢。

    ```python
    from haystack.dataclasses import ChatMessage
    from haystack.components.generators.chat import OpenAIChatGenerator
    from haystack.components.generators.utils import print_streaming_chunk

    # 創建消息列表，包含系統消息和用戶查詢
    messages = [
        ChatMessage.from_system(
            "不要假設將哪些值插入函數中。如果用戶要求不明確，請要求澄清。"
        ),
        ChatMessage.from_user("你能告訴我 Mark 住在哪裡嗎？"),
    ]

    # 初始化 OpenAIChatGenerator
    chat_generator = OpenAIChatGenerator(
        model="gpt-4-turbo",
        streaming_callback=print_streaming_chunk
    )
    # 傳入消息和工具列表並運行
    response = chat_generator.run(
        messages=messages,
        generation_kwargs={"tools": tools}
    )
    # 輸出查看
    print(response)
    ```

<br>

2. 將獲得一個以 JSON 格式顯示且包含 `工具名稱` 和 `參數` 的 `ChatMessage`。

    ```python
    {
        'replies': [
            ChatMessage(
                content='[{"index": 0, "id": "call_2ARyzeivzPqS0ETx3jVHt4ct", "function": {"arguments": "{\\"query\\":\\"Where does Mark live?\\"}", "name": "rag_pipeline_func"}, "type": "function"}]',
                role=<ChatRole.ASSISTANT: 'assistant'>,
                name=None,
                meta={
                    'model': 'gpt-4-turbo-2024-04-09',
                    'index': 0,
                    'finish_reason': 'tool_calls',
                    'usage': {}
                }
            )
        ]
    }
    ```

<br>

3. 接下來將消息內容字串解析為 JSON 並使用提供的參數調用相應的函數。

    ```python
    import json

    # 解析函數調用信息
    # 提取第一個回應中的 content
    content = response['replies'][0].content

    # 將 content 解析為 JSON
    # content 是一個 JSON 字串，需要轉換為 Python 字典
    function_calls = json.loads(content)

    # 提取第一個函數調用信息
    # 提取函數調用列表中的第一個元素
    function_call = function_calls[0]

    # 獲取函數名稱
    # 獲取函數名稱，這是我們需要調用的函數
    function_name = function_call['function']['name']

    # 解析函數參數
    # 將參數解析為字典格式
    function_args = json.loads(function_call['function']['arguments'])

    # 打印函數名稱和參數
    print("Function Name:", function_name)
    print("Function Arguments:", function_args)

    # 定義可用的函數
    def rag_pipeline_func(query: str):
        # 這裡假設你的 `rag_pipeline_func` 函數定義
        return {"reply": f"Mark lives in Berlin, query was: {query}"}

    def get_current_weather(location: str):
        # 這裡假設你的 `get_current_weather` 函數定義
        return {"weather": "sunny", "temperature": 20, "location": location}

    # 可用函數字典
    available_functions = {
        "rag_pipeline_func": rag_pipeline_func,
        "get_current_weather": get_current_weather
    }

    # 查找相應的函數並使用給定的參數調用它
    if function_name in available_functions:
        # 根據函數名稱找到對應的函數
        function_to_call = available_functions[function_name]
        # 使用解包操作將參數傳遞給函數
        function_response = function_to_call(**function_args)
        # 打印函數的返回值
        print("Function Response:", function_response)
    else:
        # 如果函數名稱未找到，打印錯誤訊息
        print(f"Function {function_name} not found.")
    ```

<br>

4. 得到以下的輸出結果。

    ```bash
    Function Name: rag_pipeline_func
    Function Arguments: {'query': 'Mark lives in which location?'}
    Function Response: {'reply': 'Mark lives in Berlin, query was: Mark lives in which location?'}
    ```

<br>

5. 最後一步，通過將函數回應附加到消息列表作為新消息，使用 `ChatMessage.from_function()` 並重新運行 `OpenAIChatGenerator`，讓模型總結結果。

    ```python
    from haystack.dataclasses import ChatMessage

    # 創建函數回應消息
    function_message = ChatMessage.from_function(
        content=json.dumps(function_response),
        name=function_name
    )
    # 將函數回應消息添加到消息列表
    messages.append(function_message)

    # 再次運行 OpenAIChatGenerator
    response = chat_generator.run(
        messages=messages,
        generation_kwargs={"tools": tools}
    )
    ```

<br>

6. 輸出。

    ![](images/img_38.png)

<br>

## 構建聊天應用程序

1. `OpenAI Chat Completions API` 並不會直接調用函數；相反，模型會生成可以在代碼中調用的 JSON。因此，為了構建 `端到端` 的聊天應用程序，需要在每次消息中檢查 `OpenAI` 回應是否為 `工具調用`。如果是，需要使用提供的參數調用相應的函數，並將函數回應發送回 OpenAI。否則，將用戶和消息都附加到消息列表中，與模型進行常規對話。

<br>

2. 要為應用程序構建一個漂亮的用戶界面，可以使用帶有聊天界面的 `Gradio`。安裝 `gradio`，運行下面的代碼單元，並使用輸入框與具有訪問權限的聊天應用程序進行交互。

    ```bash
    pip install gradio
    ```

<br>

3. 雖然 `gradio` 已成功安裝，但出現了一些依賴性衝突，這是因為 `farm-haystack` 需要的 `pydantic` 版本與 `gradio` 需要的版本不相容，`farm-haystack` 要求 pydantic 的版本必須 `小於 2`，但安裝的 pydantic 版本是 `2.7.3`，這裡先忽略不管，看看後續運作情況再來處理。

    ![](images/img_39.png)

<br>

4. 可以嘗試的查詢。

    ```bash
    "瑞典的首都是什麼？"：一個基本的查詢，沒有任何函數調用。
    "你能告訴我 Giorgio 住在哪裡嗎？"：一個基本的查詢，帶有一次函數調用。
    "馬德里的天氣怎麼樣？"、"那裡現在是晴天嗎？"：查看消息是否被記錄並發送。
    "Jean 住的地方天氣怎麼樣？"：強制調用兩次函數。
    "今天的天氣怎麼樣？"：強制 OpenAI 詢問更多澄清問題。
    ```

<br>

5. 程式碼。

    ```python
    import gradio as gr
    import json

    from haystack.dataclasses import ChatMessage
    from haystack.components.generators.chat import OpenAIChatGenerator

    chat_generator = OpenAIChatGenerator(model="gpt-3.5-turbo")
    response = None
    messages = [
        ChatMessage.from_system(
            "不要假設將哪些值插入函數中。"
            "如果用戶要求不明確，請要求澄清。"
        )
    ]

    # 定義聊天機器人函數
    def chatbot_with_fc(message, history):
        messages.append(ChatMessage.from_user(message))
        response = chat_generator.run(messages=messages, generation_kwargs={"tools": tools})

        while True:
            # 如果 OpenAI 回應是一個工具調用
            if response and response["replies"][0].meta["finish_reason"] == "tool_calls":
                function_calls = json.loads(response["replies"][0].content)
                print(response["replies"][0])
                for function_call in function_calls:
                    # 解析函數調用信息
                    function_name = function_call["function"]["name"]
                    function_args = json.loads(function_call["function"]["arguments"])

                    # 查找相應的函數並使用給定的參數調用它
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call(function_args)

                    # 使用 `ChatMessage.from_function` 將函數回應添加到消息列表
                    messages.append(ChatMessage.from_function(content=json.dumps(function_response), name=function_name))
                    response = chat_generator.run(messages=messages, generation_kwargs={"tools": tools})

            # 常規對話
            else:
                messages.append(response["replies"][0])
                break
        return response["replies"][0].content

    # 創建聊天界面
    demo = gr.ChatInterface(
        fn=chatbot_with_fc,
        # 顯示在下方的範例欄位
        examples=[
            "你能告訴我 Giorgio 住在哪裡嗎？",
            "Madrid 的天氣怎麼樣？",
            "誰住在 London?",
            "Mark 住的地方的天氣怎麼樣？",
        ],
        title="請詢問有關天氣或人們居住的地方。",
    )
    ```

<br>

6. 啟動聊天視窗。

    ```python
    # 啟動聊天應用程序
    demo.launch()
    ```

<br>

7. 啟動 `Gradio` 的視窗界面。

    ![](images/img_40.png)

<br>

___

_END_