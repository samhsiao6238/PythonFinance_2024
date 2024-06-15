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

1. 無伺服器：無需自行管理伺服器基礎設施，僅需專注於代碼邏輯。

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

1. 程式碼：`main.py`。

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

2. 必要文件 `requirements.txt`：列出需要的 Python 包，若無則保留空的文件內容。

    ```plaintext
    # 空的或列出需要的 Python 包
    ```

<br>

3. 部署指令。

    ```bash
    gcloud functions deploy hello_world --runtime python311 --trigger-http --allow-unauthenticated
    ```

<br>

___

_END_