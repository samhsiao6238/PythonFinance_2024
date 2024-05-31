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

## 創建資料庫和用戶

1. 進入 PostgreSQL 控制台。

    ```bash
    psql -U postgres
    ```

<br>

2. 使用資料庫語言創建新的資料庫和用戶。

    ```sql
    CREATE DATABASE mydatabase;
    CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
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
        user="myuser",
        password="mypassword",
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

___

_END_