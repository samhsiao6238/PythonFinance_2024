# Discord 聊天機器人

_關於 Discord [桌面版](https://discord.com/) 的下載及安裝這裡省略，請自行操作。_

<br>

<img src="images/img_20.png" width="500px" />

<br>

## 建立 Discord 機器人

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications) 並登錄 Discord 帳戶；可使用手機 App 掃碼登入。

    <img src="images/img_21.png" width="500px" />

<br>

2. 登入後，點擊右上角 `New Application` 建立新的應用。

    <img src="images/img_01.png" width="150px">

<br>

3. `命名` 並 `勾選同意`，接著點擊 `Create`。

    <img src="images/img_02.png" width="400px">

<br>

4. 切換到機器人 `Bot` 頁籤。

    <img src="images/img_03.png" width="150px">

<br>

5. 第一次建立，先點擊一次 `Reset Token`。

    <img src="images/img_04.png" width="150px">

<br>

6. 在彈出的視窗中點擊 `Yes, do it!`。

    <img src="images/img_05.png" width="400px">

<br>

7. 若有開啟雙重認證，會要求輸入驗證碼。

    <img src="images/img_22.png" width="400px">

<br>

8. 通過認證後會顯示 `A new token was generated! Be sure to copy it as it will not be shown to you again.`。

    <img src="images/img_26.png" width="550px">

<br>

9. 在 TTOKEN 區塊顯示的是機器人登入 Discord 的密鑰，可點擊 `Copy` 將 Token 記錄下來備用，之後將儲存在 `.env` 文件中作為敏感資訊處理。

    <img src="images/img_06.png" width="550px">

<br>

## 設定 Gateway Intents

_決定機器人能接收到哪些事件，也就是設定了機器人的功能與行為範圍；特別注意，當機器人加入的伺服器數量達到 100 或更多時，Intents 需要進行驗證和批准。_

<br>

1. 向下滑動到 `Privileged Gateway Intents` 區塊，三個功能都點選 `Save Change`。

    <img src="images/img_15.png" width="550px">

<br>

2. 有變更時，下方會彈出提醒儲存的視窗，點擊 `Save Changes`。

    <img src="images/img_27.png" width="550px">

<br>

## 說明 Gateway Intents

_補充說明前面開啟的三個設定_

<br>

1. `Presence Intent (存在狀態意圖)` 可允許機器人接收使用者的存在狀態更新事件，例如 `在線`、`離線`、`忙碌`等，適用於需要使用者在線狀態的情境。

<br>

2. `Server Members Intent (伺服器成員意圖)` 可允許機器人接收與伺服器成員有關的事件，例如成員的加入、離開、更新等，適用於管理伺服器成員、執行歡迎訊息或紀錄成員變動等情境。

<br>

3. `Message Content Intent (訊息內容意圖)` 可允許機器人接收大部分訊息中的訊息內容，適用於機器人需要回應或分析訊息內容的情境，例如關鍵字觸發功能或聊天機器人功能。

<br>

## 設置機器人的權限

1. 切換到 `OAuth2` 頁籤，向下滑動到 `OAuth2 URL Generator`。

    <img src="images/img_07.png" width="400px">

<br>

2. 勾選 `Scopes` 區域中的 `bot`。

    <img src="images/img_08.png" width="400px">

<br>

3. 在 `Bot Permissions` 區塊中勾選 `Administrator`，賦予機器人所有權限。

    <img src="images/img_09.png" width="200px">

<br>

4. 向下滑動到 `Generated URL` 區塊，這是邀請機器人到伺服器中的連結，複製連結並進行訪問便可完成邀請。

    <img src="images/img_10.png" width="550px">

<br>

5. 生成並打開邀請連結，邀請機器人加入伺服器。

    <img src="images/img_11.png" width="400px">

<br>

6. 會顯示專案名稱以及授權項目，預設已經打勾，點擊 `授權 Authorize`。

    <img src="images/img_12.png" width="400px">

<br>

7. 成功，前往 sam38's server。

    <img src="images/img_13.png" width="400px">

<br>

8. 點擊右上角人像圖標顯示或隱藏 `Member List`，可看到建立完成的機器人在腳本尚未運行前的狀態是 `Offline`。

    <img src="images/img_24.png" width="400px">

<br>

9. 在後續的步驟中，一但腳本運行後，狀態就會顯示為 `Online`。

    <img src="images/img_25.png" width="400px">

<br>

___

_END_