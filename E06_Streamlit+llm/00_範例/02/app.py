import streamlit as st
import anthropic


ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
anthropic_api_key = ANTHROPIC_API_KEY
# with st.sidebar:
#     # anthropic_api_key = st.text_input(
#     #     "Anthropic API Key", key="file_qa_api_key", type="password"
#     # )
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("📝 File Q&A with Anthropic")

# 文件上傳控件，允許上傳txt和md格式的文章
uploaded_file = st.file_uploader(
    "Upload an article",
    type=("txt", "md")
)
# 提示用戶輸入關於文章的問題
question = st.text_input(
    "請提出與文章相關的問題。",
    placeholder="例如：請提供我文章摘要。",
    disabled=not uploaded_file,
)

# 如果上傳了文件且輸入了問題但沒有提供API密鑰，顯示提示訊息
if uploaded_file and question and not anthropic_api_key:
    st.info("請加入你的 Anthropic API key 來繼續。")

# 如果上傳了文件且輸入了問題並且提供了API密鑰，執行以下操作
if uploaded_file and question and anthropic_api_key:
    # 讀取並解碼上傳的文章文件
    article = uploaded_file.read().decode()
    # 建立給Anthropic API的提示語，包含文章內容和用戶問題
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
    {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

    # 使用提供的API密鑰建立Anthropic API客戶端
    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        # 傳遞建立好的提示語
        prompt=prompt,
        # 定義停止序列
        stop_sequences=[anthropic.HUMAN_PROMPT],
        # 選擇使用的模型，可以更改為"claude-2"來使用Claude 2模型
        model="claude-v1",
        # 最大token數，限制回應的長度
        max_tokens_to_sample=200,
    )
    
    # 顯示答案的標題
    st.write("### Answer")
    # 寫出API返回的回應
    st.write(response.completion)
