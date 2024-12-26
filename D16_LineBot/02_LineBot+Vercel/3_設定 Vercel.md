# 設置 Vercel

<br>

## 安裝套件

1. 進入 [官網登入](https://vercel.com/login)，選擇 `Github` 登入即可。

    ![](images/img_132.png)

<br>

2. 點擊右上方的 `Docs` 文件查看相關設置的說明。

    ![](images/img_133.png)

<br>

3. 進入教程。

    ![](images/img_134.png)

<br>

4. 使用 `npm` 進行安裝。

    ![](images/img_135.png)

<br>

5. 記得要加上 `sudo`，否則安裝過程中會報錯。

    ```bash
    sudo npm i -g vercel
    ```
<br>

## 補充說明

_說明前面步驟設定的 `.env` 文件_

<br>

1. 在做任何的部署之前，都要確保腳本中的敏感資訊是否得到保護，在官方的腳本中，並未將 `secret` 以及 `token` 進行保護，這裡展示透過 `dotenv` 來隱藏敏感資訊。

    ![](images/img_136.png)

<br>

2. 安裝套件。

    ```bash
    pip install python-dotenv
    ```

<br>

3. 在專案內根目錄自建立一格隱藏檔案 `.env` 並編輯內容。

    ```bash
    _CHANNEL_ACCESS_TOKEN_ = <貼上 TKOKEN>
    _CHANNEL_SECRET_ = <貼上 SECRET>
    ```

<br>

4. 特別注意， `.env` 檔案內的字串無需加上引號，與等號間有無間隔皆可。
    
    ![](images/img_137.png)

<br>

5. 在根目錄添加 `.gitignore` 檔案，並將 `.env` 寫入其中。

    ![](images/img_138.png)

<br>

6. 在主腳本 `index.py` 導入 dotenv。

    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv()
    ```

<br>

7. 在程序中使用 `os` 來取得 Token 及 Secret。

    _取得_
    ```python
    CHANNEL_ACCESS_TOKEN = os.getenv("_CHANNEL_ACCESS_TOKEN_")
    CHANNEL_SECRET = os.getenv("_CHANNEL_SECRET_")
    ```
    _使用_
    ```
    configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(CHANNEL_SECRET)
    ```

<br>

8. 重新運行一次腳本，然後進行對話測試，確認沒問題，便可以進行以下步驟。

    ![](images/img_139.png)

_以上完成敏感資訊處理_

<br>

## 進行設定與部署

_透過 Vercel CLI 進行部署，進入根目錄中開啟終端機，務必確認是在根目錄_

<br>

1. 運行 CLI。

    ```bash
    sudo vercel
    ```

<br>

2. 執行後會出現對話。

    ![](images/img_140.png)

</br>

3. 使用 `Github` 進行登入。

    ![](images/img_141.png)

<br>

4. 成功登入後會顯示如下畫面，不會自動返回終端機，要手動切換。

    ![](images/img_142.png)

<br>

5. 表示這個專案資料夾並非是一個 `repo`，詢問是否設置並且部署：`Y`。

    ![](images/img_143.png)

<br>

## 開始設定專案

1. 選擇當前的專案。

    ![](images/img_144.png)

<br>

2. 不要連結現有專案：`N`。

    ![](images/img_145.png)

<br>

3. 專案名稱，使用預設即可，按下 `ENTER`。
    
    ![](images/img_146.png)

<br>

4. 在哪個目錄，同樣使用預設，按下 `ENTER` 即可。

    ![](images/img_147.png)

<br>

5. 假如沒有提供預設名稱，則手動輸入。

    ![](images/img_153.png)

</br>

## 錯誤排除

_若因版本問題出現錯誤，請依以下步驟排除，若順利完成，可跳過此步驟。_

<br>

1. 出現如下錯誤。

    ![](images/img_151.png)

<br>

2. 進入 Vercel 控制台中在前面步驟所建立的專案中，點擊 `Settings`。

    ![](images/img_155.png) 

<br>

1. 在 `General` 頁籤中找到 `Node.js Version`，手動切換到 `18.0`。

    ![](images/img_150.png)

<br>

4. 切換後記得儲存 `Save`。

    ![](images/img_152.png)

<br>

5. 再次透過 `sudo vercel` 指令進行設定。

    ![](images/img_54.png)

<br>

## 開始部署

_以上程序完成後會提示進行部署_

<br>

1. 提示進行部署。

    ![](images/img_154.png)

<br>

2. 使用以下指令進行部署，切記加上 `sudo`。

    ```bash
    sudo vercel --prod
    ```

<br>

3. 完成部署，而訊息中顯示因為 `builds` 已經存在於設置檔案中，所以設置沒有套用，這並不影響部署的完成。

    ![](images/img_156.png)

<br>

4. 另外依據說明，這並非一個 repo，這在之後的步驟會進行部署，這裡暫不理會。

    ![](images/img_157.png)

</br>

## 前往 Vercel 主控台

1. 進入 Vercel 並開啟 `主控台`。

    ![](images/img_17.png)

<br>

2. 會顯示前面步驟上傳的專案，點擊進入。

    ![](images/img_69.png)

</br>

3. 先複製 Domain，可能會有兩個以上的 URL，任意複製一個即可。

    ![](images/img_70.png)

<br>

4. 開啟瀏覽器進行訪問所複製的網址，這個時頁會顯示如下錯誤，_不用理會_。

    ![](images/img_158.png)

</br>

## 前往 Line Developers

1. 回到 `Line Developers` 編輯 `Webhook`。

    ![](images/img_71.png)

</br>

2. 貼上網址，保有原本的尾綴 `/callback`，然後點擊 `Update`。

    ![](images/img_72.png)

</br>

3. 再次強調，這個尾綴 `callback` 是定義在 `index.py` 中的路由，若使用其他範例，務必檢查尾綴是否為 `\callback`，很多時候也會使用 `\webhook`。

    ![](images/img_73.png)

</br>

4. 確認 `Use webhook` 是開啟。

    ![](images/img_74.png)

</br>

5. 這時還沒完成設定，點擊驗證會是錯的。

    ![](images/img_76.png)

</br>

6. 繼續進行設定，點擊 Edit。

    ![](images/img_78.png)

</br>

7. 選擇接受邀請。

    ![](images/img_79.png)

</br>

8. 總的來說是這樣。

    ![](images/img_80.png)

</br>

_🔺 以上完成第一階段的 Line Developers 設定_

</br>

## 回到 Vercel

1. 進入 Vercel 後切換到頁籤 `Settings`。

    ![](images/img_81.png)

</br>

2. 點擊左側 `Enviroment Variables`，這是設定服務器的環境變數。

    ![](images/img_82.png)

</br>

3. 複製 `.env` 文件中的兩個環境變數名稱作為 Key。

    ![](images/img_83.png)

</br>

4. 先貼上 Key。

    ![](images/img_84.png)

<br>

5. 再貼上對應的的值。

    ![](images/img_159.png)

</br>

6. 務必點擊 `Save` 進行儲存。

    ![](images/img_85.png)

<br>

7. 儲存後會顯示在 `Settings` 的最下方。

    ![](images/img_160.png)

</br>

## F. 進入 VSCode

1. 將專案發佈到新的儲存庫中。

   ![](images/img_86.png)

</br>

2. 選公開。

   ![](images/img_87.png)

</br>

3. 完成部署在 Github 上查看。

    ![](images/img_161.png)

<br>

## G. 再回到 Vercel 中

1. 點擊連結到專案。

   ![](images/img_88.png)

</br>

2. 選取 GitHub。

   ![](images/img_89.png)

</br>

3. 連結對應的專案，在這裡是 `mybot`。

    ![](images/img_90.png)

</br>

4. 回到產品部署 `Production Deployment` 的畫面，可以點擊 `Source code` 查看內容以確認是否為更新的內容。

   ![](images/img_91.png)

</br>

## H. 驗證結果

1. Vercel 的部署有時會有延遲狀況，可以透過去修改一下 `index.py` 來同步並觀察一下部署狀況。

   ![](images/img_92.png)

</br>

2. 直到畫面正常顯示就表示部署完成。

   ![](images/img_93.png)

</br>

3. 也可以透過驗證 Webhook 確認是否完成部署。

   ![](images/img_94.png)

</br>

## I. 其他補充

    _介紹完伺服器後，再使用 `Ngrok` 將 LineBot 部署在樹莓派上_

</br>

---

_END:這裡僅是確認部署，至於腳本內容並無太多功能_