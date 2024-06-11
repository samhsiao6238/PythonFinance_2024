# LangChain

<br>

## 介紹

_LangChain 是一個強大的框架，目的是簡化語言模型應用的開發，提供了一整套工具和功能來建立、管理和擴展語言模型應用，包括代理、工具、提示管理等。_

<br>

## `langchain.agents` 的 `initialize_agent`、`AgentType` 方法

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain
    ```

<br>

2. 導入：

    ```python
    from langchain.agents import initialize_agent, AgentType
    ```

<br>

3. LangChain 提供了一個框架來建立語言模型應用，包括代理、工具、提示管理等。

<br>

4. `initialize_agent` 用於初始化一個代理。

<br>

5. `AgentType` 用於指定代理的類型。

<br>

## `langchain.callbacks` 的 `StreamlitCallbackHandler` 方法

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain
    ```

<br>

2. 導入：

    ```python
    from langchain.callbacks import StreamlitCallbackHandler
    ```

<br>

3. 主要功能：`StreamlitCallbackHandler` 是 LangChain 提供的回調處理器，可在 Streamlit 應用中顯示代理的想法和操作。

<br>

## `langchain.chat_models` 的 `ChatOpenAI` 方法

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain
    ```

<br>

2. 導入：

    ```python
    from langchain.chat_models import ChatOpenAI
    ```

<br>

3. 主要功能：`ChatOpenAI` 是 LangChain 提供的聊天模型接口，用於與 OpenAI 的聊天模型進行互動。

<br>

## `langchain.tools` 的 `DuckDuckGoSearchRun` 方法

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain
    ```

<br>

2. 導入：

    ```python
    from langchain.tools import DuckDuckGoSearchRun
    ```

<br>

3. 主要功能：`DuckDuckGoSearchRun` 用於在代理中進行 DuckDuckGo 搜索。

<br>

## `langchain.prompts` 的 `PromptTemplate` 方法

_LangChain 於 2021 年發布_

<br>

1. 安裝：

    ```bash
    pip install langchain
    ```

<br>

2. 導入：

    ```python
    from langchain.prompts import PromptTemplate
    ```

<br>

3. 主要功能：LangChain 提供的提示模板工具，用於建立和管理提示。

<br>

___

_END_