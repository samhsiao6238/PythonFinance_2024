# 介紹

以下將透過範例演繹如何使用 `Streamlit` 加上 `OpenAI` 等相關套件進行聊天機器人專案。




```python
import streamlit as st
from openai import OpenAI
```

```python
import streamlit as st
import anthropic
```

```python
import streamlit as st
# 用於初始化代理
from langchain.agents import initialize_agent, AgentType
# 用於處理回調
from langchain.callbacks import StreamlitCallbackHandler
# 用於使用OpenAI的聊天模型
from langchain.chat_models import ChatOpenAI
# 用於進行DuckDuckGo的搜索
from langchain.tools import DuckDuckGoSearchRun
```

```python
import streamlit as st
from langchain.llms import OpenAI
```

```python
import streamlit as st
# 使用 langchain_openai 的 ChatOpenAI
from langchain_openai import ChatOpenAI
# 引入 LangChain 的 PromptTemplate 模組，用於創建 `提示模板`
from langchain.prompts import PromptTemplate
# 加入正則表達
import re
```

```python
# 使用 openai 的 OpenAI
from openai import OpenAI
import streamlit as st
# streamlit_feedback 用於收集用戶反饋
# 每次回應後會顯示一個反饋界面，讓用戶對語言模型的回應進行評價
from streamlit_feedback import streamlit_feedback
# trubrics 用於存儲和處理用戶反饋
import trubrics
```