# callback_manager

<br>

1. 在 `Ollama` 模型初始化過程中，參數 `callback_manager` 用以設置 `回調管理器`，用來處理模型執行過程中的各種事件，比如輸出數據流或處理錯誤。

2. `CallbackManager` 類可用來管理和調用多個回調處理器的工具。

3. 回調處理器 `Callback Handler` 是實現特定行為的函數，這些行為包括但不限於模型輸出新數據、處理結束、出現錯誤等，會在特定事件發生時被觸發。

4. `StreamingStdOutCallbackHandler` 是一個回調處理器，它的作用是將模型的輸出實時地打印到終端，這在需要監控或調試模型輸出時非常有用。

<br>

## 範例及解釋

1. 以下是初始化 `Ollama` 模型並設置回調管理器的範例。

    ```python
    from langchain.callbacks import (
        CallbackManager,
        StreamingStdOutCallbackHandler
    )
    from langchain_community.llms import Ollama

    # 初始化模型並設置回調管理器
    llm = Ollama(
        model="llama3",
        callback_manager=CallbackManager(
            [StreamingStdOutCallbackHandler()]
        )
    )
    ```

<br>

### 詳細說明

1. CallbackManager:

   - `CallbackManager` 是一個用來管理多個回調處理器的工具。
   - 可以將多個回調處理器添加到 `CallbackManager` 中，這樣在事件發生時，所有的回調處理器都會被 _依次調用_。

<br>

2. StreamingStdOutCallbackHandler:

   - `StreamingStdOutCallbackHandler` 是一個特定的回調處理器，它的作用是將模型的輸出實時地打印到終端機中。

<br>

3. 設置回調管理器:
   - 在初始化 `Ollama` 模型時，通過 `callback_manager` 參數傳入一個 `CallbackManager` 實例。
   - `CallbackManager` 實例中包含一個或多個回調處理器，例如 `StreamingStdOutCallbackHandler`。

<br>

___

_END_