# 安裝 PostgreSQL

<br>

## 說明

_MacOS_

<br>

1. 如果尚未安裝 PostgreSQL，使用 Homebrew 來安裝。

    ```bash
    brew install postgresql@15
    ```

<br>

2. 透過 `brew services` 來啟動服務。

    ```bash
    brew services start postgresql@15
    ```

<br>

3. 檢查服務的狀態來確保其已啟動。

    ```bash
    brew services list
    ```

<br>

4. 停止服務。

    ```bash
    brew services stop postgresql@15
    ```

<br>

___

_END_