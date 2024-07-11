# Discord 聊天機器人

<img src="images/img_20.png" width="500px" />

<br>

## 建立 Discord 機器人

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications) 並登錄 Discord 帳戶。

    <img src="images/img_21.png" width="500px" />

<br>

2. 點擊 `New Application` 。

    ![](images/img_01.png)

<br>

3. 命名後勾選同意，接著點擊 `Create`。

    ![](images/img_02.png)

<br>

4. 切換到 `機器人 Bot` 頁籤。

    ![](images/img_03.png)

<br>

5. 第一次建立，先點擊一次 `Reset Token`。

    ![](images/img_04.png)

<br>

6. 點擊 `Yes, do it!`。

    ![](images/img_05.png)

<br>

7. 若有開啟雙重認證，會要求輸入驗證碼。

    ![](images/img_22.png)

<br>

8. 滑動到 `Privileged Gateway Intents` ，三個功能都點選 `Save Change`。

    ![](images/img_15.png)

<br>

9. 點擊 `Copy` 將 Token 記錄下來，貼到 `.env` 文件中；這是機器人登入 Discord 的密鑰。

    ![](images/img_06.png)

<br>

## 設置機器人的權限

1. 切換到 `OAuth2` 頁籤，選擇 `URL Generator`。

    ![](images/img_07.png)

<br>

2. 勾選 `bot`。

    ![](images/img_08.png)

<br>

3. 在 `Bot Permissions` 勾選 `Administrator`，賦予機器人所有權限。

    ![](images/img_09.png)

<br>

4. 複製連結進行訪問，這是邀請機器人到伺服器中的連結。

    ![](images/img_10.png)

<br>

5. 生成並打開邀請連結，邀請機器人加入伺服器。

    ![](images/img_11.png)

<br>

6. 點擊 `授權 Authorize`。

    ![](images/img_12.png)

<br>

7. 成功，前往 sam38's server。

    ![](images/img_13.png)

<br>

___

_END_