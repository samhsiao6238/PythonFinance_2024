from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")

app = Flask(__name__)

# 設定 LINE Messaging API 回應 URL
LINE_REPLY_API = "https://api.line.me/v2/bot/message/reply"

# 設定 HTTP Headers
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
}

def send_reply(reply_token, messages):
    """發送回應訊息到 LINE"""
    data = {
        "replyToken": reply_token,
        "messages": messages
    }
    response = requests.post(LINE_REPLY_API, headers=HEADERS, json=data)
    return response.status_code, response.text

@app.route("/webhook", methods=["POST"])
def webhook():
    """處理 LINE Webhook 事件"""
    body = request.json
    print("收到的 Webhook 資料:", body)

    if "events" in body:
        for event in body["events"]:
            # 取得回應 Token
            reply_token = event.get("replyToken", "")
            
            # 取得來源資訊
            source = event.get("source", {})
            user_id = source.get("userId", "未知使用者")
            group_id = source.get("groupId", "非群組")

            # 建立回應訊息
            reply_messages = [
                {"type": "text", "text": f"你的 User ID: {user_id}"},
                {"type": "text", "text": f"群組 ID: {group_id}"}
            ]

            # 發送回應
            send_reply(reply_token, reply_messages)

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5050, debug=True)
