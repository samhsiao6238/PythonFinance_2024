# 建立 LineBot

_實作：本實作會以建立 LineBot 為例，介紹 Vercel 與 GitHub 整合。_

</br>

## 步驟

_以下是在 MacOS 中操作，若在 Win 系統操作，將中終端機指令改為 cmd 指令，或使用面板操作相關檔案建立的步驟即可。_

<br>

1. 開啟終端機，透過指令建立並進入專案目錄，這裡示範在 `桌面` 建立 `_test02_`；專案路徑及名稱可自行修正。

   ```bash
   cd ~/Desktop && mkdir _test02_ && cd _test02_
   ```

</br>

2. 在專案資料夾內開啟新的 VSCode 工作區。

   ```bash
   code .
   ```

</br>

3. 若要部署在 `Vercel`，需建立如下的資料結構。

   ```bash
   mkdir api && touch api/index.py && touch requirements.txt vercel.json .env
   ```

   ![img](images/img_51.png)

</br>

## 範例程式

_以下代碼是參考 [Line 官方 Github](https://github.com/line/line-bot-sdk-python/blob/master/examples/flask-echo/app_with_handler.py) 後略作修改的腳本，使用開啟的 VSCode 進行編輯。_

</br>

1. 建立並啟動虛擬環境，這裡不再贅述。

<br>

2. 先安裝套件。

   ```bash
   python -m pip install line-bot-sdk flask python-dotenv
   ```

</br>

3. 在 VSCode 中編輯 `api` 資料夾內的文件 `index.py`，複製以下內容貼上即可。

   ```python
   import os
   import sys
   from argparse import ArgumentParser

   from flask import Flask, request, abort
   from linebot.v3 import (
      WebhookHandler
   )
   from linebot.v3.exceptions import (
      InvalidSignatureError
   )
   from linebot.v3.webhooks import (
      MessageEvent,
      TextMessageContent,
   )
   from linebot.v3.messaging import (
      Configuration,
      ApiClient,
      MessagingApi,
      ReplyMessageRequest,
      TextMessage
   )

   import os
   from dotenv import load_dotenv
   load_dotenv()

   app = Flask(__name__)


   channel_secret = os.getenv('CHANNEL_SECRET', None)
   channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
   if channel_secret is None:
      print('Specify LINE_CHANNEL_SECRET as environment variable.')
      sys.exit(1)
   if channel_access_token is None:
      print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
      sys.exit(1)

   handler = WebhookHandler(channel_secret)

   configuration = Configuration(
      access_token=channel_access_token
   )


   @app.route("/callback", methods=['POST'])
   def callback():
      # get X-Line-Signature header value
      signature = request.headers['X-Line-Signature']

      # get request body as text
      body = request.get_data(as_text=True)
      app.logger.info("Request body: " + body)

      # handle webhook body
      try:
         handler.handle(body, signature)
      except InvalidSignatureError:
         abort(400)

      return 'OK'


   @handler.add(MessageEvent, message=TextMessageContent)
   def message_text(event):
      with ApiClient(configuration) as api_client:
         line_bot_api = MessagingApi(api_client)
         line_bot_api.reply_message_with_http_info(
               ReplyMessageRequest(
                  reply_token=event.reply_token,
                  messages=[TextMessage(text=event.message.text)]
               )
         )


   if __name__ == "__main__":
      arg_parser = ArgumentParser(
         usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
      )
      arg_parser.add_argument('-p', '--port', default=8000, help='port')
      arg_parser.add_argument('-d', '--debug', default=False, help='debug')
      options = arg_parser.parse_args()

      app.run(debug=options.debug, port=options.port)

   ```

</br>

4. 編輯 `.env` 文件，先貼上以下內容。

   ```json
   CHANNEL_ACCESS_TOKEN=<填入自己的 Token>
   CHANNEL_SECRET=<填入自己的 Secret>
   ```

<br>

## 進入 Line Developer

_特別注意，這並非唯一的進入程序，只要能進入設定畫面並進行設定皆可。_

<br>

1. 進入 [中文官網](https://developers.line.biz/zh-hant/) 。

<br>

2. 點擊 `Messaging API`。

   ![](images/img_102.png)

<br>

3. 點擊 `開始體驗`，另外文件在製作筆記的同時是 `404` 的。

   ![](images/img_103.png)

<br>

4. 使用自己的帳號登入。

   ![](images/img_104.png)

_若有其他步驟請依據使用經驗自行判斷，應該沒難度。_

<br>

## 建立機器人

1. 建立 `channel`，首先要選擇現有的 `Provider` 或是建立新的，這裡示範建立名為 `Test_0412` 的 Provider。

   ![](images/img_105.png)

<br>

2. 區域設定為 `Taiwan`，接著在設定 `Email address` 之前的其餘項目皆可 _任意輸入_。

   ![](images/img_106.png)

<br>

3. 勾選兩個同意選項之後點擊建立 `Create`。

   ![](images/img_107.png)

<br>

4. 點擊 `OK`。

   ![](images/img_108.png)

<br>

5. 點擊同意 `Agree`。

   ![](images/img_109.png)

<br>

6. 以上完成建立並進入開發介面。

   ![](images/img_110.png)

<br>

## 取得憑證

_先取得 `secret` 以及 `token`_

<br>

1. 首先取得 `secret` 並記錄在 `.env` 文件中的 `CHANNEL_SECRET`。

   ![](images/img_111.png)

<br>

2. 日後若要重新設定新的 `secret` 則點擊 `issue` 即可。

   ![](images/img_112.png)

<br>

3. 切換到 `Messaging API` 頁籤。

   ![](images/img_113.png)

<br>

4. 點擊 `issue` 建立新的 `token` 並記錄在 `.env` 文件中的 `CHANNEL_SECRET`。

   ![](images/img_114.png)

<br>

5. 日後要更新則點擊 `Reissue` 即可。

   ![](images/img_115.png)

_以上完成初步建置，接著回到腳本編輯。_

<br>

## 編輯專案

_回到專案資料夾中繼續編輯腳本_

<br>

1. 編輯套件管理檔案 `requirements.txt` ，套件有版本相容問題，所以要加上版本號，無論是否使用 `Vercel` 作為部署服務器，都還是可建立這個管理檔案的，有利於未來重建專案時的版本管理。

   ```txt
   Flask==2.2.2
   line-bot-sdk
   Werkzeug==2.3.7
   ```

</br>

2. 編輯 Vercel 設定檔案 `vercel.json`，這是給部署在服務器上使用的設定文件。

   ```json
   {
      "builds": [
         {
            "src": "api/index.py",
            "use": "@vercel/python"
         }
      ],
      "routes": [
         {
            "src": "/(.*)",
            "dest": "api/index.py"
         }
      ]
   }
   ```

</br>

3. 在 `api` 資料夾開啟終端機。

   ![](images/img_116.png)

<br>

4. 運行腳本。

   ```bash
   python index.py
   ```

<br>

5. 會出現紅色警告，暫時不予理會。

   ![](images/img_117.png)

<br>

6. 啟動 `ngrok`，在同樣的端口上運行。

   ```bash
   ./ngrok http 5000
   ```

<br>

7. 這裡要特別說明一點，以上的程序看似都沒問題，但因為在 `macOS Monterey` 以上的版本中自帶的 `AirPlay Receiver` 服務會佔用 `5000` 端口，所以後續進行 `webhook` 設定時會出現 `Error`，所以 MacOS 使用者可對腳本進行修改，指定使用其他端口如 `5001`。

   ```python
   if __name__ == "__main__":
      app.run('0.0.0.0', port=5001)
   ```

<br>

8. 特別注意，若有修改時要重新指定 `ngrok` 的服務端口與腳本相同。

   ```bash
   ./ngrok http 5001
   ```

<br>

9. 複製網址。

   ![](images/img_118.png)

<br>

10. 進入 `Line Developer` 介面進行 `webhook` 設定，在 `Messaging API` 頁籤中進行編輯 `Edit`。

   ![](images/img_119.png)

<br>

11. 特別注意，先查看一下腳本中的路由設置，範例專案是設定為 `/callback`，有時也常用 `/webhook`。

   ![](images/img_120.png)

<br>

12. 貼上 `ngrok` 提供的網址以及路由。

   ![](images/img_121.png)

<br>

13. 開啟 `Use webhook`，並點擊 `Verify` 進行驗證以確認設定是否正確。

   ![](images/img_122.png)

<br>

14. 成功時會顯示 `Success`。

   ![](images/img_123.png)

<br>

15. 始用手機掃描條碼來添加好友。

   ![](images/img_124.png)

<br>

16. 點擊加入好友後會直接跳出歡迎對話。

   ![](images/img_125.png)

<br>

17. 接著進行 `LINE Official Account features` 的設定。

   ![](images/img_126.png)

<br>

18. 添加相片，在這裡添加相片可對相片進行縮放，而在建立帳號的時候添加相片將無法進行縮放，所以建議在這個步驟添加相片，每次添加後一個小時內無法變更。

   ![](images/img_127.png)

<br>

19. 接受加入群組以及接收文字以外訊息可拓展更多機器人的功能。

   ![](images/img_128.png)

<br>

20. 這時透過對話發送一個 `你好` 的訊息，會發現機器人回覆了兩個訊息，其中第一個是 `自動回覆`，而第二個是腳本中撰寫的回應相同內容的訊息。

   ![](images/img_130.png)

<br>

21. 可在 `回應設定` 頁籤中關閉 `自動回應訊息`，之後就透過腳本編程來進行回應。

   ![](images/img_129.png)

<br>

22. 再次發送訊息，機器人便只會回應相同內容。

   ![](images/img_131.png)

<br>

___

_以上完成初步的設置_
