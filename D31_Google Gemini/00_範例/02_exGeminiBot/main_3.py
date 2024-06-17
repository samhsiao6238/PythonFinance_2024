from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import json
import os
from firebase import firebase
import google.generativeai as genai
from PIL import Image
from google.cloud import storage

# 使用環境變數讀取憑證
token = os.getenv("LINE_BOT_TOKEN")
secret = os.getenv("LINE_BOT_SECRET")
firebase_url = os.getenv("FIREBASE_URL")
gemini_key = os.getenv("GEMINI_API_KEY")
storage_bucket = os.getenv("STORAGE_BUCKET")

# 初始化 Gemini Pro API
genai.configure(api_key=gemini_key)

# 初始化 Google Cloud Storage 客戶端
storage_client = storage.Client()
bucket = storage_client.bucket(storage_bucket)


def linebot(request):
    # 取得請求的原始數據並轉換為文本
    body = request.get_data(as_text=True)
    # 將文本數據轉換為 JSON 格式
    json_data = json.loads(body)
    try:
        # 建立 LineBotApi 實例以便與 LINE 平台交互
        line_bot_api = LineBotApi(token)
        # 建立 WebhookHandler 實例以處理 LINE 消息
        handler = WebhookHandler(secret)
        # 取得請求頭中的簽名
        signature = request.headers["X-Line-Signature"]
        # 驗證請求並處理消息
        handler.handle(body, signature)
        # 取得消息事件的第一個事件
        event = json_data["events"][0]
        # 取得回覆令牌
        tk = event["replyToken"]
        # 取得發送消息的用戶 ID
        user_id = event["source"]["userId"]
        # 取得消息類型
        msg_type = event["message"]["type"]
        # 建立 Firebase 應用實例
        fdb = firebase.FirebaseApplication(firebase_url, None)
        # 定義用戶聊天記錄的路徑
        user_chat_path = f"chat/{user_id}"
        # 從 Firebase 取得用戶的聊天記錄
        chatgpt = fdb.get(user_chat_path, None)

        # 假如是文本訊息
        if msg_type == "text":
            # 取得文字消息的文本內容
            msg = event["message"]["text"]

            if chatgpt is None:
                # 如果沒有聊天記錄，建立空列表
                messages = []
            else:
                # 否則，使用已有的聊天記錄
                messages = chatgpt

            # 檢查是否為 "!清空" 或全形 "！清空"
            if msg.replace("！", "!") == "!清空":
                # 如果消息是 "!清空"，回覆清空提示
                reply_msg = TextSendMessage(text="對話歷史紀錄已經清空！")
                # 刪除用戶的聊天記錄
                fdb.delete(user_chat_path, None)
                # 刪除 Google Cloud Storage 中相關圖片
                blobs = bucket.list_blobs(prefix=f"images/{user_id}/")
                for blob in blobs:
                    blob.delete()  # 刪除圖片
            else:
                # 建立 Gemini Pro 模型
                model = genai.GenerativeModel("gemini-pro")
                # 將用戶消息加入聊天記錄
                messages.append({"role": "user", "parts": [msg]})
                # 使用 Gemini Pro 生成回覆
                response = model.generate_content(messages)
                # 將模型回覆加入聊天記錄
                messages.append({"role": "model", "parts": [response.text]})
                # 將模型回覆轉換為 LINE 消息
                reply_msg = TextSendMessage(text=response.text)
                # 更新 Firebase 中的對話紀錄
                fdb.put_async(user_chat_path, None, messages)
            # 使用 LINE Bot API 發送回覆消息
            line_bot_api.reply_message(tk, reply_msg)

        elif msg_type == "image":
            # 接收到圖片消息
            print("接收到圖片消息")
            # 取得圖片消息的 ID
            message_id = event["message"]["id"]
            # 取得圖片內容
            message_content = line_bot_api.get_message_content(message_id)

            with open(f"/tmp/{message_id}.jpg", "wb") as fd:
                # 將圖片內容寫入文件
                fd.write(message_content.content)

            # 打開圖片並轉換為 PIL 格式
            img = Image.open(f"/tmp/{message_id}.jpg")

            # 上傳圖片到 Firebase Storage
            storage_path = f"images/{user_id}/{message_id}.jpg"
            blob = bucket.blob(storage_path)
            blob.upload_from_filename(
                f"/tmp/{message_id}.jpg", content_type="image/jpeg"
            )
            blob.make_public()
            image_url = blob.public_url

            # 將圖片 URL 存入 Firebase
            if chatgpt is None:
                messages = []
            else:
                messages = chatgpt
            # 添加圖片消息記錄
            messages.append({"role": "user", "type": "image", "url": image_url})
            # 更新 Firebase 中的對話紀錄
            fdb.put_async(user_chat_path, None, messages)

            # 定義生成圖片描述的提示
            prompt = "你是一個專業的攝影師，請對以下圖片進行描述與解說："
            # 建立 Gemini Pro Vision 模型
            model = genai.GenerativeModel("gemini-pro-vision")
            # 生成圖片描述
            response = model.generate_content([prompt, img], stream=True)
            response.resolve()

            # 將生成的圖片描述轉換為 LINE 消息
            reply_msg = TextSendMessage(text=response.text)

            # 將機器人的描述消息也添加到 Firebase
            messages.append({"role": "model", "parts": [response.text]})
            fdb.put_async(user_chat_path, None, messages)

            # 發送回覆訊息
            line_bot_api.reply_message(tk, reply_msg)

        else:
            # 如果消息不是文字或圖片，回覆提示
            reply_msg = TextSendMessage(text="你發送的不是文字或圖片訊息喔！")
            # 使用 LINE Bot API 發送回覆消息
            line_bot_api.reply_message(tk, reply_msg)

    except Exception as e:
        detail = e.args[0]
        print(detail)
    # OK 表示處理完成
    return "OK"
