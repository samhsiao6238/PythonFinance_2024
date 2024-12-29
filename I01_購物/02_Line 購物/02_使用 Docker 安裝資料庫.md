# MariaDB

_在 NAS 使用 Docker 部署資料庫_

<br>

## 連線

_在本機開啟終端機_

<br>

1. 連線 NAS。

    ```bash
    ssh sam6238@nas
    ```

<br>

2. 切換為超級用戶；這個指令將以 `root` 權限啟動新的 `shell`，允許在該 `shell` 中執行需要 `sudo` 權限的命令，且不必每次都在加 `sudo` 或輸入密碼。

    ```bash
    sudo -s
    ```

    ![](images/img_02.png)

<br>

## 容器

1. 檢查是否已安裝 Docker。

    ```bash
    docker -v
    ```

    ![](images/img_03.png)

<br>

2. 查詢當前鏡像，並篩選關鍵字 `mariadb`，確定尚未下載相關鏡像。

    ```bash
    docker images | grep mariadb
    ```

<br>

3. 拉取 MariaDB 鏡像。

    ```bash
    docker pull mariadb:latest
    ```

    ![](images/img_04.png)

<br>

4. 檢查是否成功拉取 `mariadb:latest`。

    ```bash
    docker images
    ```

    ![](images/img_05.png)

<br>

## 建立數據目錄

1. 查看當前預設目錄內的數據。

    ```bash
    ls /volume1/docker/
    ```

<br>

2. 建立儲存 `數據` 與 `配置` 的目錄。

    ```bash
    mkdir -p /volume1/docker/mariadb/data /volume1/docker/mariadb/conf
    ```

<br>

3. 查看建立後的目錄；補充說明，在 NAS 中並無 `tree` 指令。

    ```bash
    ls /volume1/docker/mariadb/
    ```

<br>

## 啟動容器

1. 先建立帳號密碼等變數；以下要輸入自己的帳號密碼，因為資料庫密碼並無敏感性，這裡不做遮蔽，僅遮蔽 NAS 密碼。

    ```bash
    export MYSQL_USER=sam6238
    export MYSQL_PASSWORD=sam112233
    export MYSQL_DATABASE=testdb
    export MYSQL_ROOT_PASSWORD=<NAS-的密碼>
    ```

<br>

2. 可透過 `echo` 指令加上 `$` 提取變數，確認皆已正確設置。

    ```bash
    echo $MYSQL_USER $MYSQL_PASSWORD $MYSQL_DATABASE $MYSQL_ROOT_PASSWORD
    ```

<br>

3. 啟動 MariaDB 容器，並設置端口、帳號和密碼。

    ```bash
    docker run -d \
    --name mariadb \
    -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
    -e MYSQL_DATABASE=$MYSQL_DATABASE \
    -e MYSQL_USER=$MYSQL_USER \
    -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
    -p 3306:3306 \
    -v /volume1/docker/mariadb/data:/var/lib/mysql \
    mariadb:latest
    ```

    ![](images/img_06.png)

<br>

4. 補充說明，建立後所傳回的是 `新建立的容器的 ID`，這是容器的唯一標識符；`容器 ID` 是一個 `64 字元` 的十六進制字串，但在一般操作上僅需 `前 12 個字元`，所以運行 `docker ps` 指令時，顯示的就是這個字串。

    ```bash
    docker ps
    ```

    ![](images/img_17.png)

<br>

## 參數說明

1. `-d`：在後台運行容器。

<br>

2. `-p 3306:3306`：將宿主機的 `3306` 端口映射到容器的 `3306` 端口。

<br>

3. `-v /volume1/docker/mariadb/data:/var/lib/mysql`：將數據目錄掛載到宿主機。

<br>

## 檢查容器狀態

1. 查看容器是否運行中。

    ```bash
    docker ps
    ```

    ![](images/img_07.png)

<br>

2. 查看 MariaDB 的日誌，確認是否正常啟動。

    ```bash
    docker logs mariadb
    ```

<br>

## 測試連線

_在 NAS 中要使用 `mariadb` 的 CLI 客戶端連線到 MariaDB_

<br>

1. 在宿主機測試連線，這裡使用 `root` 連線，所以要輸入的是 NAS 的密碼；宿主機就是 NAS，也就是安裝容器的主機。

    ```bash
    docker exec -it mariadb mariadb -u root -p
    ```

    ![](images/img_08.png)

<br>

2. 退出；退出可不用分號 `;`。

    ```sql
    exit;
    ```

<br>

3. 若使用前面步驟建立的帳號 `sam6238` 連線，則輸入該帳號的密碼。

    ```bash
    docker exec -it mariadb mariadb -u sam6238 -p
    ```

<br>

## 運行資料庫

1. 查看現有資料庫。

    ```sql
    SHOW DATABASES;
    ```

<br>

2. 切換到特定資料庫 `testdb`。

    ```sql
    USE testdb;
    ```

<br>

3. 建立新資料庫

    ```sql
    CREATE DATABASE newdb_test;
    ```

<br>

4. 然後確認資料庫是否建立成功。

    ```sql
    SHOW DATABASES;
    ```

    ![](images/img_09.png)

<br>

5. 選取資料庫；指令使用大小寫皆可，`大寫` 語句只是資料庫的慣用表達方式，音易讀性較高，並可與 Linux 指令區隔，建議使用。

    ```sql
    use testdb;
    ```

    ![](images/img_10.png)

<br>

6. 查看資料表；當前尚無資料表。

    ```sql
    SHOW TABLES;
    ```

<br>

## 建立新用戶

1. 查詢當前正在使用資料庫的用戶訊息。

    ```sql
    SELECT USER();
    ```

    ![](images/img_11.png)

<br>

2. 查看當前用戶的權限，結果表明用戶能夠登錄 MariaDB，但無法對資料庫執行任何操作，除非有其他授權。

    ```bash
    SHOW GRANTS FOR CURRENT_USER();
    ```

    ![](images/img_12.png)

<br>

## 切換到 root 帳號

_以下將授權部分分開處理以說明各項權限_

<br>

1. 直接在當前用戶指令下切換到管理員；其中 `\!` 表示執行的是系統指令，接著要輸入的是 root 的密碼，也就是 NAS 密碼。

    ```sql
    \! mariadb -u root -p
    ```

    ![](images/img_13.png)

<br>

2. 授予 `全部權限`，特別注意，這個 `全部` 是僅針對資料庫 `testdb` 授予所有表的全部操作權限。

    ```sql
    GRANT ALL PRIVILEGES ON testdb.* TO 'sam6238'@'%';
    FLUSH PRIVILEGES;
    ```

<br>

3. 在前一項的基礎上，可授予 `GRANT OPTION` 權限給 `sam6238`，允許該用戶將該權限授予其他用戶。

    ```sql
    GRANT ALL PRIVILEGES ON testdb.* TO 'sam6238'@'%' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```

<br>


4. 授予指定用戶 `SELECT` 權限，也就是授予對 `mysql.user` 表的查詢權限。

    ```sql
    GRANT SELECT ON mysql.user TO 'sam6238'@'%';
    FLUSH PRIVILEGES;
    ```

<br>

5. 授予 `CREATE USER` 權限，也就是針對 `所有資料庫（*.*）` 授予 `建立用戶` 的權限。

    ```sql
    GRANT CREATE USER ON *.* TO 'sam6238'@'%';
    FLUSH PRIVILEGES;
    ```

<br>

6. 還要授予 `RELOAD` 權限，也就是針對 `所有資料庫（*.*）` 授予 `刷新權限表` 的權限。

    ```sql
    GRANT RELOAD ON *.* TO 'sam6238'@'%';
    FLUSH PRIVILEGES;
    ```

<br>

7. 以上語句可一次性表達。

    ```sql
    GRANT ALL PRIVILEGES ON testdb.* TO 'sam6238'@'%' WITH GRANT OPTION;
    GRANT SELECT ON mysql.user TO 'sam6238'@'%';
    GRANT CREATE USER, RELOAD ON *.* TO 'sam6238'@'%';
    FLUSH PRIVILEGES;
    ```

<br>

8. 再次切換帳號到 `sam6238`。

    ```sql
    \! mariadb -u sam6238 -p
    ```

<br>

9. 查看當前用戶的權限；以下顯示當前用戶 `sam6238@%` 的所有權限。

    ```sql
    SHOW GRANTS FOR CURRENT_USER();
    ```

    ![](images/img_14.png)

<br>

## 操作資料庫

1. 查看所有用戶及其主機訊息。

    ```sql
    SELECT User, Host FROM mysql.user;
    ```

    ![](images/img_15.png)

<br>

2. 若要建立用戶、授權、確保插件、刷新授權。

    ```sql
    CREATE USER 'sam6239'@'%' IDENTIFIED BY 'sam112233';
    GRANT ALL PRIVILEGES ON testdb.* TO 'sam6239'@'%';
    ALTER USER 'sam6239'@'%' IDENTIFIED VIA mysql_native_password USING PASSWORD('sam112233');
    FLUSH PRIVILEGES;
    ```

<br>

3. 確認用戶是否正確建立。

    ```sql
    SELECT User, Host, Plugin FROM mysql.user WHERE User = 'sam6239';
    ```

    ![](images/img_16.png)

<br>

4. 若要刪除帳號 `sam6239`。

    ```sql
    DROP USER IF EXISTS 'sam6239'@'%';
    ```

<br>

___

_END_