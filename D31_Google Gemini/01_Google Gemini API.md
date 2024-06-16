# Google Gemini API

## 參考 

1. _[官網](https://ai.google.dev/aistudio?hl=zh-tw)_

![](images/img_54.png)

2. [範例文本](https://medium.com/@proflead/ai-chatbot-python-and-gemini-api-tutorial-for-beginners-c809b08bfe8c) 及 [範例 GitHub](https://github.com/proflead/gemini-flask-app/tree/master)。

## 

1. 安裝套件

```bash
pip install Flask langchain-core langchain-google-genai
```

2. 建立環境變數

```python
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
```