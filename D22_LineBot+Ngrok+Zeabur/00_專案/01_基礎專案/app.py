from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# 導入所需的函式庫並調用函數讀取 .env 的值
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
app = Flask(__name__)
# 改寫
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/")
def home():
    return "<h1>歡迎光臨我的首頁</h1>"


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature."
            " Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):

    '''添加以下代碼'''
    _text = ""
    if event.message.type != "text":
        _text = "我只能接收文字訊息 > <"
    elif event.message.text == "說話":
        _text = "我可以說話囉，歡迎來跟我互動 ^_^ "
    elif event.message.text == "閉嘴":
        _text = "好的，我閉嘴 > <"
    else:
        _text = "我不明你想表達什麼 > <"

    # 建立了一個 API client 實例，使用在 configuration 中定義的配置。
    # with 語句確保在該代碼區塊執行結束後可釋放資源。
    with ApiClient(configuration) as api_client:
        # 使用客戶端實例初始化一個 MessagingApi 物件，用於後續的消息操作。
        line_bot_api = MessagingApi(api_client)
        # 使用這個實例調用回覆訊息的函數
        line_bot_api.reply_message_with_http_info(
            # 回應訊息
            ReplyMessageRequest(
                # 透過 event 取的回應的 token，這是用以確認回應對象的
                reply_token=event.reply_token,
                # 這是具體回應的內容
                messages=[
                    # 將回應訊息改為 _text
                    TextMessage(text=_text)
                ]
            )
        )


if __name__ == "__main__":
    app.run('0.0.0.0', port=5001)
