# 模組介紹

_以下介紹 `OpenAI` 相關模組_

<br>

## `OpenAI`

_OpenAI API 於 2020 年發布_

<br>

1. 安裝：

    ```bash
    pip install openai
    ```

<br>

2. 導入：

    ```python
    from openai import OpenAI
    ```

<br>

3. 這是 OpenAI 官方提供的 API 客戶端模組，直接與 OpenAI 的 GPT-3、GPT-4 等模型進行互動，提供生成文本、完成任務等功能。

<br>

## `langchain.llms` 的 `OpenAI`

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain
    ```

<br>

2. 導入：

    ```python
    from langchain.llms import OpenAI
    ```

<br>

3. 主要功能：LangChain 提供的語言模型接口，用於與 OpenAI 的模型進行交互。

<br>

4. 差異：這個 `OpenAI` 是 LangChain 封裝的接口，旨在簡化在 LangChain 框架內與 OpenAI 模型的交互。

<br>

## `langchain_openai` 的 `ChatOpenAI`

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain-openai
    ```

<br>

2. 導入：

    ```python
    from langchain_openai import ChatOpenAI
    ```

<br>

3. 主要功能：LangChain OpenAI 提供的聊天模型接口，用於與 OpenAI 的聊天模型進行交互，適用於 LangChain 的擴展包。

<br>

## _補充說明_

<br>

_openai、langchain.llms 中的 OpenAI、langchain.chat_models 中的 ChatOpenAI。_

1. openai 中的 OpenAI 是 OpenAI 官方提供的底層 API 客戶端，直接與 OpenAI 的服務器通信，提供了完整的 OpenAI API 功能，適合需要利用所有 OpenAI API 功能的場景。

2. langchain.llms 中的 OpenAI 是 LangChain 提供的高階封裝，集成了 LangChain 的功能，並簡化了在 LangChain 應用中使用 OpenAI 的過程，適合在 LangChain 生態系統中使用，並與 LangChain 的其他功能無縫集成，這個模組使用上會依賴於 LangChain 框架，安裝時須留意。

3. langchain.chat_models 中的 ChatOpenAI：專為聊天模型設計的接口，簡化了與 OpenAI 聊天模型的互動，適合需要使用聊天模型並集成 LangChain 高級功能的場景。

<br>

___

_END_