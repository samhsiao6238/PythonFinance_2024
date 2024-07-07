# 安裝 PostgreSQL

<br>

## 說明

_MacOS_

<br>

1. 安裝前，先檢查是否已經安裝或安裝版本。

    ```bash
    brew services list
    ```

<br>

2. 如果尚未安裝 PostgreSQL，使用 Homebrew 來安裝。

    ```bash
    brew install postgresql@15
    ```

<br>

3. 透過 `brew services` 來啟動服務。

    ```bash
    brew services start postgresql@15
    ```

<br>

4. 檢查服務的狀態來確保其已啟動。

    ```bash
    brew services list
    ```

<br>

5. 停止服務。

    ```bash
    brew services stop postgresql@15
    ```

<br>

6. 卸載 PostgreSQL 15。

    ```bash
    brew uninstall postgresql@15
    ```

<br>

7. 因為 `pgvector` 可能依賴於 PostgreSQL 導致無法卸載，可以先卸載 `pgvector`。

    ```bash
    brew uninstall pgvector
    ```

<br>

8. 重新安裝時，可先安裝 `postgresql@15` 再安裝 `pgvector`，確保與新安裝的 PostgreSQL 兼容。

    ```bash
    brew install pgvector
    ```

<br>

___

_END_