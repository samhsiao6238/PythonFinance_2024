# invoke

_方法說明_

<br>

# 說明

1. `llm_model.invoke()` 是用於調用指定的語言模型生成響應的函數，在這個範例裡是 `Ollama` 模型。

<br>

2. `llm_model` 是語言模型 `Ollama` 類已經初始化的實例，這個類是導入自 `langchain_community.llms`，可以說是在 `LangChain` 應用中使用 `Ollama` 聊天模型，所以相關文件在 `Ollama` 可能找不到，要去 `LangChain` 說明中查詢。

    ```python
    from langchain_community.llms import Ollama

    llm = Ollama(model="llama3")
    llm.invoke("Tell me a joke")
    ```

<br>

3. `invoke` 方法用於調用模型並生成回應，接受一個或多個參數，這些參數構成了模型需要處理的輸入，例如傳遞了包含模板及用戶問題的字串 `prompt_template`，在這個範例中，模板內要求模型 _只用繁體中文回答_，但這樣的請求未必能得到百分百的滿足。

<br>

4. 本範例部分代碼。

    ```python
    from langchain_community.llms import Ollama

    # 初始化 Ollama 模型
    llm_model = Ollama(model="llama3")

    # 構建提示模板
    prompt_template = """
    你是一個專門回答問題的聊天機器人，
    你的名字是「Yollama」，
    你擁有各種高階專業學術知識，
    請回答以下問題：
    請只以繁體中文回答：這是一個範例問題。
    """

    # 使用 invoke 方法生成響應
    response = llm_model.invoke(prompt_template)

    # 打印響應
    print(response)
    ```

<br>

___

_END_