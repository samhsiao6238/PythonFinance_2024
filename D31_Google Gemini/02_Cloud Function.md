# Python Cloud Function 概述

<br>

## 說明

1. `Cloud Function` 是一種 `無伺服器` 運算模型，允許開發者撰寫並執行輕量級的、獨立的小程式片段，這些小程式被稱為 `函數（Function）`。

<br>

2. 這些函數會在特定的事件發生時被觸發執行，例如 `HTTP 請求`、`數據庫變更`、`Cloud Pub/Sub 消息` 等。

<br>

3. 主要雲端服務提供商如 Google Cloud、AWS、Azure 都支持以 Python 編寫的 Cloud Functions。

<br>

## 特點

1. 無伺服器：無需自行管理伺服器基礎設施，僅需專注於程式碼邏輯。

2. 事件驅動：函數會在指定事件發生時自動執行。

3. 自動擴展：根據流量需求自動擴展和縮減運算資源。

4. 高效開發：專注於業務邏輯，無需處理伺服器管理和基礎設施維護。

5. 靈活擴展：根據需求自動擴展，無需手動調整資源。

6. 節省成本：按使用量計費，無需長期預付大量資源費用。

<br>

## 用途

1. API 驅動的應用：可以作為 API 端點來處理 HTTP 請求。

2. 後端服務：如數據處理、文件轉換、消息通知等。

3. 事件響應：處理各類事件，如數據庫觸發、檔案上傳等。

4. Webhooks：處理外部系統的 Webhook 回調。

5. 微服務：構建分散的小型服務，負責不同的業務邏輯。

6. 數據處理：如圖片處理、數據轉換和格式化等。

<br>

## 核心概念

1. 函數入口：函數的主邏輯。對於 HTTP 觸發器，它通常是一個處理 HTTP 請求的函數。

<br>

2. 事件驅動：函數會根據特定事件被觸發執行。事件來源包括 HTTP 請求、Pub/Sub 消息、Cloud Storage 變更等。

<br>

3. 環境變數：可以通過環境變數配置函數的運行時參數，如 API 金鑰、資料庫 URL 等。

<br>

## 建立與部署

1. 建立 Cloud Function：使用 Google Cloud Console 或 gcloud CLI 建立 Cloud Function，設定函數觸發方式（例如：HTTP、Pub/Sub）。

<br>

2. 編寫 Python 程式碼：在本地撰寫 Python 程式碼，並包含必要的函數入口。確保包括所有依賴包在 `requirements.txt` 中。

<br>

3. 部署到 Google Cloud：使用 Google Cloud Console 或 gcloud CLI 部署程式碼。

<br>

## 範例

_簡單的 Python Cloud Function 範例，可回應一個 HTTP 請求並返回 "Hello, World!"_

<br>

1. 建立本地資料夾。


    ```bash
    mkdir python-cloud-function
    cd python-cloud-function
    ```

2. 編輯 `requirements.txt`。

    ```plaintext
    # 此文件可以是空的，或列出需要的 Python 包
    ```

3. 編寫 `main.py`。

    ```python
    def hello_world(request):
        """HTTP Cloud Function.
        Args:
            request (flask.Request): The request object.
            Returns:
            The response text, or any set of values that can be turned into a
            Response object using `make_response`.
        """
        return 'Hello, World!'
    ```

<br>

## 登錄 Google Cloud Console

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)。

<br>

2. 選擇或創建一個新的 Google Cloud 專案。

<br>

3. 搜尋並啟用 `Cloud Functions API`。

<br>

4. 導航到 `Cloud Functions`，點擊「Create Function」。

<br>

5. 設定 Cloud Function：函數名稱：`hello-world-function`、區域選擇靠近的區域即可、觸發器選擇 `HTTPS`，允許未經身份驗證的請求。

<br>

6. 設置運行環境 Runtime：選擇 `Python 3.11`。

<br>

7. 上傳 `requirements.txt`（如果有依賴包）。

8. 貼上 `main.py` 程式碼。

```python
def hello_world(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    return 'Hello, World!'
```

<br>

9. 設置進入點：在「Function to execute」字段中輸入 `hello_world`。

<br>

10. 部署 Cloud Function：點擊「Deploy」來部署函數。

<br>

# 測試 Cloud Function

1. 部署完成後，記錄下生成的 URL（例如 `https://<your-region>-<your-project-id>.cloudfunctions.net/hello-world-function`）。

2. 在瀏覽器中訪問該 URL，應看到返回的 "Hello, World!" 字樣。

<br>

## 特別注意

1. 確保定期檢查和管理已部署的 Cloud Functions，避免產生不必要的費用。

2. 可以刪除不再使用的函數，避免浪費資源。

<br>

___

_END_