# 建立 PostgreSQL 資料庫

_可以在本機或雲端進行，這裡示範在本機安裝。_

<br>

## 安裝工具或套件

1. Windows：下載 PostgreSQL 安裝程式 [PostgreSQL Download](https://www.postgresql.org/download/) 後執行並按照指示完成安裝即可。

<br>

2. macOS：使用 Homebrew 安裝 PostgreSQL。

    ```bash
    brew install postgresql
    ```

<br>

3. Linux：使用 apt 或 yum 安裝。

    ```bash
    # 使用 apt 安裝（Ubuntu/Debian）
    sudo apt update
    sudo apt install postgresql postgresql-contrib

    # 使用 yum 安裝（CentOS/RHEL）
    sudo yum install postgresql-server postgresql-contrib
    ```

<br>

## 本機啟動服務

1. Windows：在安裝過程中，PostgreSQL 服務應該已經啟動，可以通過 `服務管理器`檢查。

<br>

2. macOS/Linux：啟動 PostgreSQL 服務。

    ```bash
    # macOS
    brew services start postgresql
    # Linux
    sudo systemctl start postgresql
    ```

<br>

## 建立資料庫和用戶

1. 進入 PostgreSQL 控制台。

    ```bash
    psql -U postgres
    ```

<br>

2. 使用資料庫語言建立新的資料庫 `mydatabase`。

    ```sql
    CREATE DATABASE mydatabase;
    ```

<br>

3. 建立用戶 `sam6238`，並自訂密碼，_特別注意_，這裡的帳戶名稱是 `sam6238`。

    ```sql
    CREATE USER sam6238 WITH ENCRYPTED PASSWORD '<輸入自訂的密碼>';
    ```

<br>

4. 授權用戶 `sam6238` 對於資料庫 `mydatabase` 擁有權限。
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE mydatabase TO sam6238;
    ```

<br>

## 範例程式碼

_連接到 PostgreSQL 資料庫_

<br>

1. 程式碼

    ```python
    import psycopg2
    from psycopg2 import sql

    # 使用 psycopg2 連接到 PostgreSQL 資料庫
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="sam6238",
        password="<輸入自訂的密碼>",
        # 如果是本機，使用 "localhost"
        # 如果是雲端，使用雲端資料庫的終端點
        host="localhost",
        port="5432"
    )

    # 建立游標以執行 SQL 查詢
    cur = conn.cursor()

    # 執行範例查詢
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"Database version: {db_version}")

    # 關閉游標和連接
    cur.close()
    conn.close()
    ```

<br>


2. 完成連線會顯示。
```bash
Database version: ('PostgreSQL 15.5 on aarch64-apple-darwin21.6.0, compiled by Apple clang version 14.0.0 (clang-1400.0.29.102), 64-bit',)
```

<br>

___

_END_