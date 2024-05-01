
# 建立容器 

_在 VScode 中建立，以下紀錄簡化的步驟_

<br>

## 基礎建置

1. 建立本機一個專案資料夾並啟動 VSCode。

<br>

2. 新增容器設定檔。

    ![](images/img_01.png)

<br>

3. 選擇新增至工作區或使用者資料夾皆可，這裡示範添加到工作區。

    ![](images/img_02.png)

<br>

4. 選取 `Python`。

    ![](images/img_03.png)

<br>

5. 容器底層的操作系統是 Debian，所以提供選取其版本號，這裡使用新版的 `bullseye`。

    ![](images/img_04.png)

<br>

6. 其他功能先不選取，這裡點擊 `確定` 跳過即可。

    ![](images/img_05.png)

<br>

7. 接著點擊右下方的 `在容器中重新開啟` 按鈕。

    ![](images/img_18.png)

<br>

8. 點擊重建 `Rebuild` 。

    ![](images/img_19.png)

<br>

9. 在工作區中會添加兩個資料夾並各有一個文件，分別是 `.devcontainer ` 中有文件 `devcontainer.json`，`.github` 中有文件 `dependabot.yml`。

    ![](images/img_06.png)

<br>

10. 假如容器尚未連線，可點擊左下角的連線。

    ![](images/img_09.png)

<br>

11. 啟動。

    ![](images/img_07.png)

<br>

12. 右下角會出現當前狀態訊息。

    ![](images/img_08.png)

<br>

13. 允許。

    ![](images/img_10.png)

<br>

14. 完成後左下角會出現容器資訊。

    ![](images/img_11.png)

<br>

15. 在終端機中查詢，會顯示容器的相關版本訊息。

    ![](images/img_12.png)

<br>

16. 預設的容器設定文件 `devcontainer.json` 內容如下，特別注意，這個版本號是 VSCode 建立容器時自動生成的。

    ```json
    // For format details, see https://aka.ms/devcontainer.json. For config options, see the
    // README at: https://github.com/devcontainers/templates/tree/main/src/python
    {
        "name": "Python 3",
        // Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
        "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye"

        // Features to add to the dev container. More info: https://containers.dev/features.
        // "features": {},

        // Use 'forwardPorts' to make a list of ports inside the container available locally.
        // "forwardPorts": [],

        // Use 'postCreateCommand' to run commands after the container is created.
        // "postCreateCommand": "pip3 install --user -r requirements.txt",

        // Configure tool-specific properties.
        // "customizations": {},

        // Uncomment to connect as root instead. More info: https://aka.ms/dev-containers-non-root.
        // "remoteUser": "root"
    }
    ```

<br>

17. 修改如下。

    ```json
    {
        "name": "Python 3.12.3",
        "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",
        "postCreateCommand": "pip install --upgrade pip"
    }
    ```

18. 可將自己原本的 `settings.json` 融入到容器的設置文件 `devcontainer.json` 中，這裡以我自己的為例。

    ```json
    {
        "name": "Python 3.12.3",
        "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",
        "postCreateCommand": "pip install --upgrade pip",
        "customizations": {
            "vscode": {
                "settings": {
                    "pasteImage.path": "${currentFileDir}/images/",
                    "pasteImage.namePrefix": "img_",
                    "pasteImage.defaultName": "0",
                    "pasteImage.showFilePathConfirmInputBox": true,
                    "flake8.args": [
                        "--max-line-length=200",
                        "--ignore=E402"
                    ]
                },
                "extensions": ["ms-python.python"]
            }
        }
    }
    ```

<br>

19. 修改過設定文件後要重新 rebuild。

    ![](images/img_13.png)

<br>

20. 完成後會出現以下訊息。

    ![](images/img_14.png)

<br>

## 建立 Dockerfile

1. 在資料夾 `.devcontainer` 中建立文件 `Dockerfile`。

    ![](images/img_15.png)

<br>

2. 依照指示安裝 Docker。

    ![](images/img_16.png)

<br>

3. 編輯文件。

    ```dockerfile
    # 使用指定映像
    FROM python:3.12-bullseye

    # 安裝必要庫
    RUN apt-get update && apt-get install -y git zsh && rm -rf /var/lib/apt/lists/*
    ```

<br>

4. 關於 Docker 文件，可以參考 [Docker Hub](https://hub.docker.com/) 的官方版本，進入後搜尋 `python`。

    ![](images/img_27.png)

<br>

5. 找到對應的版本，點擊進入後檔案內容很多，也可以使用這個版本來建立，但非常耗時，尤其在建立 Codespace 的時候，所以這裡省略。

    ![](images/img_28.png)

<br>

6. 修改配置文件 `devcontainer.json` ，將 `image` 註解起來，並指向 `Dockerfile`。

    ```json
    {
        "name": "Python 3.12.3",
        // "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",
        "build": {
            "dockerfile": "Dockerfile"
        },
        "postCreateCommand": "pip install --upgrade pip",
        "customizations": {
            "vscode": {
                "settings": {
                    "pasteImage.path": "${currentFileDir}/images/",
                    "pasteImage.namePrefix": "img_",
                    "pasteImage.defaultName": "0",
                    "pasteImage.showFilePathConfirmInputBox": true,
                    "flake8.args": [
                        "--max-line-length=200",
                        "--ignore=E402"
                    ]
                },
                "extensions": ["ms-python.python"]
            }
        }
    }
    ```

<br>

5. 再次重建 `Rebuild` ，完成後依照指示按下 `ENTER`。

    ![](images/img_17.png)

<br>

## Docker Desktop

1. 安裝桌面版 Docker 後可看到所建立的容器。

    ![](images/img_20.png)

<br>

2. 觀察容器詳情。

    ![](images/img_21.png)

<br>

## 進行版本控制

_以下示範使用 CLI_

<br>

1. 建立 Git 倉庫基礎步驟。

    ```bash
    # 初始化
    git init
    # 添加當前倉庫文件
    git add .
    # 提交
    git commit -m "init"
    # 指定分支
    git branch -M main
    ```

<br>

2. 在 Github 上建立一個新的倉庫，並記錄所提供的網址 `https://github.com/samhsiao6238/_container_.git`。

    ![](images/img_22.png)

<br>

3. 特別注意，這個階段在遠端倉庫中先不要建立 README，避免可能導致後續推送時產生衝突，該文件也不是這階段的重點，所以建議省略。

<br>

4. 另外，之後有更新時都要再次進行 `添加` 與 `提交`。

    ```bash
    # 添加當前倉庫文件
    git add .
    # 提交
    git commit -m "update"
    ```

<br>

5. 連線遠程倉庫，使用前面步驟取得的網址，同學務必換為自己的網址。

```bash
git remote add origin <遠端倉庫網址>
```

<br>

6. 推送到倉庫。

    ```bash
    git push -u origin main
    ```

<br>

7. 完成。

    ![](images/img_23.png)

<br>

8. 可為容器配置的重要版本的 Git 標籤，或使用分支來管理不同的配置版本，這有助於重建特定版本的容器。

    ```bash
    # 建立標籤與註解
    git tag -a "v1.0-container-setup" -m "Version 1.0 of container setup"
    # 推送
    git push --tags
    ```

<br>

## 啟動 Codespace

_以下展示在遠端重建倉庫_

1. 初次建立。

    ![](images/img_24.png)

<br>

2. Codespace 會自動識別倉庫中的 `.devcontainer` 配置來建立開發環境，這包含 `devcontainer.json` 和 `Dockerfile` 。

    ![](images/img_29.png)

<br>

3. 運行後等待完成連線會顯示如下視窗，接著可能會跳出關於插件安裝的視窗，特別注意，由於 Codespace 可能會有些限制導致插件未能正確安裝或使用。

    ![](images/img_30.png)

<br>

## 在遠端修改倉庫

_以更換 Python 版本號為例_

<br>

1. 進入 [Docker Hub](https://hub.docker.com/) 查詢 Python 映像的版本號。

2. 搜尋 Python 映像的版本號，這裡示範使用 `3.10`。

    ![](images/img_25.png)

<br>

3. 在倉庫中開啟 `Dockerfile` 並修改 Python 版本號，標準安裝太耗時，這裡試試使用簡易的文件。

    ```dockerfile
    # 使用指定映像
    FROM python:3.10-bullseye

    # 安裝必要庫
    RUN apt-get update && apt-get install -y git zsh && rm -rf /var/lib/apt/lists/*
    ```

<br>

4. 嘗試重新建立。

    ![](images/img_26.png)

<br>

5. 查詢後會顯示新的版本號。

    ![](images/img_31.png)

<br>

6. 提交更新後的文件並完成同步。
![](images/img_32.png)

_回到 VSCode 中_

<br>

7. 在本機的 VSCode 中點擊 `Fetch`。

    ![](images/img_33.png)

<br>

8. 完成同步。

    ![](images/img_34.png)

<br>

9. 重建容器。

    ![](images/img_35.png)

<br>

10. 如此便完成容器的同步。

    ![](images/img_36.png)

<br>

## 查詢容器與更名

1. 使用 Docker Desktop。

    ![](images/img_37.png)

<br>

2. 特別注意，容器的 `Name` 是自動分配且隨機生成的，由一對 `形容詞＋名詞` 組成，可透過以下指令進行自訂。

    ```bash
    docker rename beautiful_wilbur my-cotainer
    ```

<br>

3. 刷新就可看到。

    ![](images/img_38.png)

<br>

##  建立 docker-compose.yml

1. 先前所使用的 `devcontainer.json` 文件主要用於配置 `VSCode` 如何與容器互動，包括 _設定開發環境_、_安裝 VSCode 擴充功能_ 等，雖然在這個文件中也可以 _指定連接埠轉送的規則_ ，但這通常用於開發時的連接埠轉送需求，而不是容器服務之間的連接埠對映，所以在端口管理上，`docker-compose.yml` 文建會是更好的選擇，而 `devcontainer.json` 文件則專注在配置與 VSCode 直接相關的設置。 

<br>

2. 在 `.devcontainer` 資料夾中建立文件 `docker-compose.yml`。

<br>

3. 假設該容器將用於 Streamlit 專案使用，並將使用 MariaDB 以及 MongoDM，其端口預設分別為 `8501`、`3306`、`27017`。

    ```yaml
    version: '3.10'

    services:
    # streamlit
    streamlit:
        build:
        # 使用 Dockerfile
        context: .
        dockerfile: Dockerfile
        # 當前目錄掛載位置
        volumes:
        - .:/app
        working_dir: /app
        ports:
        - "8501:8501"
        # 先安裝依賴庫再啟動服務
        command: sh -c "pip install -r requirements.txt && streamlit run app.py"
        # 確保服務在兩者之後啟動
        depends_on:
        - mariadb
        - mongodb

    mariadb:
        # 使用官方鏡像
        image: mariadb
        # 需要手動設置這些數值
        environment:
        MYSQL_ROOT_PASSWORD: rootpassword
        MYSQL_DATABASE: exampledb
        MYSQL_USER: user
        MYSQL_PASSWORD: userpassword
        volumes:
        - mariadb_data:/var/lib/mysql
        ports:
        - "3306:3306"

    mongodb:
        image: mongo
        environment:
        MONGO_INITDB_ROOT_USERNAME: mongouser
        MONGO_INITDB_ROOT_PASSWORD: mongopassword
        volumes:
        - mongodb_data:/data/db
        ports:
        - "27017:27017"

    volumes:
    mariadb_data:
    mongodb_data:
    ```

<br>

4. 安裝 `docker-compose`，以下是三行指令。

    ```bash
    apt update && apt install -y curl
    curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ```

<br>

5. 透過查詢版本來驗證安裝。

    ```bash
    docker-compose --version
    ```

<br>

6. 回到本機中開啟終端機，並執行這個腳本來依照設置運行容器。

    ```bash
    docker-compose up -d
    ```

<br>

7. 透過這樣的設置，便可允許外部設備通過訪問主機來訪問容器中的服務。

![](images/img_39.png)

<br>

## 從外部訪問容器

_以 STreamlit 為例_

<br>

1. 建立一個範例腳本 `app.py`。

    ```python
    import streamlit as st

    st.title('Hello Streamlit in Docker!')
    st.write("This is a simple Streamlit app running inside a Docker container.")
    ```

<br>

2. 修改 Dockerfile。

    ```dockerfile
    # 使用指定映像
    FROM python:3.10-bullseye

    # 安裝必要庫，並清理快取以減少鏡像體積
    RUN apt-get update && \
        apt-get install -y git zsh && \
        rm -rf /var/lib/apt/lists/*

    # 建立一個新用戶 'appuser' 並切換到此用戶
    RUN useradd -m appuser
    USER appuser

    # 設定工作目錄
    WORKDIR /app

    # 複製目前目錄內容到容器中的 /app
    COPY . /app

    # 安裝 Streamlit
    RUN pip install --no-cache-dir streamlit

    # 使得 8501 連接埠在容器外部可存取
    EXPOSE 8501

    # 在容器啟動時執行 Streamlit
    CMD ["streamlit", "run", "app.py"]
    ```

<br>

3. 簡化 `docker-compose.yml`。

    ```yaml
    version: '3.10'

    services:
    # streamlit
    streamlit:
        build:
        # 使用 Dockerfile
        context: .
        dockerfile: Dockerfile
        # 當前目錄掛載位置
        volumes:
        - .:/app
        working_dir: /app
        ports:
        - "8501:8501"
    ```

<br>

4. 在項目資料夾內運行。

    ```bash
    docker-compose up --build
    ```

<br>

5. 完成時會顯示。

    ![](images/img_40.png)

<br>

6. 透過瀏覽器訪問。

    ![](images/img_41.png)

<br>

## 其他

1. 停止容器。

    ```bash
    docker stop my-cotainer
    ```

<br>

2. 刪除容器。

    ```bash
    docker rm my-cotainer
    ```

<br>

---

_END_