# OAuth

_可參考 [官方說明](https://ai.google.dev/gemini-api/docs/oauth?hl=zh-tw)_

![](images/img_76.png)

<br>

## 創建 OAuth 憑證

1. 進行 `模型調整` 時，而僅有 `API Key` 是不夠的，這是因為模型調整涉及敏感數據和高級操作，需要更高級別的安全性和權限管理，所以進行 `OAuth 驗證`，。

<br>

2. 展開導覽選單，滑動到 `API 與服務` 並點擊 `憑證`。

    ![](images/img_25.png)

<br>

3. 點擊 `建立憑證` 展開選單，接著點 `OAuth 客戶端 ID`。

    ![](images/img_26.png)

<br>

4. 點擊 `設定同意畫面`。

    ![](images/img_27.png)

<br>

5. 因為是自行開發和學習使用 Google Cloud 服務，建議選擇 `External` 方式，接著點擊 `建立`。

    ![](images/img_28.png)

<br>

## 應用程式資訊

1. 在 `應用程式名稱` 欄位中，輸入 `Project2024-01`，並透過下拉選單選擇電子郵件。

    ![](images/img_29.png)

<br>

2. 輸入 `開發人員聯絡資訊` 後點擊 `儲存並繼續`。

    ![](images/img_43.png)

<br>

## Edit app registration

1. 在 `授權範圍` 部分，你可以略過新增範圍，直接點擊 `儲存並繼續`；之後需要為應用程式新增範圍，可以在此步驟進行修改和驗證。

    ![](images/img_44.png)

<br>

2. 點擊 `+ ADD USERS`，在跳出的視窗中，輸入自己及其他授權測試的使用者郵件地址，並點擊 `新增`。

    ![](images/img_45.png)

<br>

3. 點擊 `儲存並繼續`。

    ![](images/img_46.png)

<br>

4. 點擊回到主控台 `BACK TO DASHBOARD`。

    ![](images/img_47.png)

<br>

## 

1. 再次點擊 `建立憑證`，選取 `OAuth 客戶端 ID`。

    ![](images/img_48.png)

<br>

2. 在 `應用程式類型` 中選擇 `電腦版應用程式`。

    ![](images/img_49.png)

<br>

3. 輸入名稱，依照畫面說明 `您的 OAuth 2.0 用戶端名稱。這個名稱只會用於在控制台中識別用戶端，不會向使用者顯示`，然後點擊 `建立`。

    ![](images/img_50.png)

<br>

4. 再跳出來的視窗中先點擊 `下載 JSON`，然後點擊 `確認`。

    ![](images/img_30.png)

<br>

5. 在下載資料夾中會看到這個憑證，這是一個 `JSON` 文件。

    ![](images/img_31.png)

<br>

6. 這個文件預設的名稱太長，可修改為 `client_secret.json`。

    ![](images/img_32.png)

<br>

## 使用本地命令進行驗證

_使用 `gcloud` 命令進行驗證_

<br>

1. 進入下載的資料夾中，運行命令將 `client_secret.json 文件` 轉換為應用程式可用的憑證，以下的 `\` 是換行符號，如果在 `Colab` 上執行，擇加上 `--no-browser` 參數。

    ```bash
    gcloud auth application-default login \
        --client-id-file=client_secret.json \
        --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/generative-language.tuning'
    ```

<br>

2. 這行指令將啟動瀏覽器，要求登錄 `Google` 帳戶並授予應用所需的權限，接著點擊 `繼續`。

    ![](images/img_33.png)

<br>

3. 點擊 `全選` 然後 `繼續`。

    ![](images/img_34.png)

<br>

4. 完成授權後，會生成一個 `Credentials` 並儲存在本地，這些憑證將由任何請求應用程式預設憑證 (ADC) 的庫使用。

    ```bash
    Credentials saved to file: [/Users/samhsiao/.config/gcloud/application_default_credentials.json]

    These credentials will be used by any library that requests Application Default Credentials (ADC).
    ```

<br>

## 使用 Curl 測試

_使用 `curl` 測試是否正常運作_

<br>

1. 使用前面步驟取得的 `access_token` 和 `project_id` 進行檢查，以下指令中需要輸入 `自己的 Project ID`。

    ```bash
    access_token=$(gcloud auth application-default print-access-token)
    project_id=<自己的 Project ID>
    ```

<br>

2. 使用 `curl` 測試以確認能夠存取 `API`。

    ```bash
    curl -X GET https://generativelanguage.googleapis.com/v1/models \
        -H 'Content-Type: application/json' \
        -H "Authorization: Bearer ${access_token}" \
        -H "x-goog-user-project: ${project_id}" | grep '"name"'
    ```

<br>

## Python 用戶端測試

1. 安裝 Google 用戶端程式庫。

    ```bash
    複製程式碼
    pip install google-generativeai
    ```

<br>

2. 使用 Python 程式碼進行測試。

    ```python
    import google.generativeai as genai

    print('Available base models:', [m.name for m in genai.list_models()])
    ```

<br>

___

_END_