# Docker 常用的 CLI 指令

<br>

1. Docker 版本查詢。

    ```bash
    docker --version
    ```

<br>

2. 查看運行中的容器。

    ```bash
    docker ps
    ```

<br>

3. 查看本地鏡像檔案列表：列出本地儲存的所有 Docker 鏡像。

    ```bash
    docker images
    ```

<br>

4. 刪除指定的本地鏡像。

    ```bash
    docker rmi <鏡像ID>
    ```

<br>

5. 從 Docker Hub 或是其他倉庫拉取指定的鏡像檔案。

    ```bash
    docker pull <鏡像名稱>
    ```

<br>

6. 根據當前資料夾內的 Dockerfile 建立新的鏡像。

    ```bash
    docker build -t <鏡像標籤> .
    ```

<br>

7. 運行指定容器：從鏡像啟動一個新容器，常用參數如 `-d` 後台運行、`-p` 端口映射、`-e` 設置環境變數。

    ```bash
    docker run [options] <鏡像名稱>
    ```

<br>

8. 停止容器運行。

    ```bash
    docker stop <容器ID>
    ```

<br>

9. 啟動停止中的容器。

    ```bash
    docker start <容器ID>
    ```

<br>

10. 刪除容器，加入參數 `-f` 可強制刪除正在執行的容器。

    ```bash
    docker rm -f <容器ID>
    ```

<br>

11. 進入容器：以互動方式進入。

    ```bash
    docker exec -it <容器ID> /bin/bash
    ```

<br>

12. 查看容器網路配置。

    ```bash
    docker network ls
    ```

<br>

13. 建立容器網路。

    ```bash
    docker network create <網路名稱>
    ```

<br>

14. 刪除容器網路。

    ```bash
    docker network rm <網路名稱>
    ```

<br>

15. 在容器中建立 `卷`。

    ```bash
    docker volume create <Volume名稱>
    ```

<br>

16. 列出容器中的卷。

    ```bash
    docker volume ls
    ```

<br>

17. 刪除容器中的卷。

    ```bash
    docker volume rm <Volume名稱>
    ```

<br>

18. 查看容器日誌。

    ```bash
    docker logs <容器ID>
    ```

<br>

19. 啟動容器服務：根據 `docker-compose.yml` 文件啟動服務。

    ```bash
    docker-compose up
    ```

<br>

20. 停止容器服務：停止並移除由 `docker-compose.yml` 文件所定義的服務。

    ```bash
    docker-compose down
    ```

<br>

___

_END_