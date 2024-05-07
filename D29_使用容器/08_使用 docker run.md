# `docker run`

_延續之前的步驟繼續操作_

<br>

## 說明

1. 建立 Docker 鏡像，命名為 `streamlit-app`。

    ```bash
    docker build -t streamlit-app .
    ```

<br>

2. 使用 `docker run` 指令啟動前一個步驟建立的容器，並透過參數 `-p` 指定端口映射，前面是 `宿主機端口`，後面是 `容器端口`。

    ```bash
    docker run -p 8501:8501 streamlit-app
    ```

<br>

3. 啟動後便能在宿主機的瀏覽器透過 `localhost:8501` 進行訪問容器的服務。

<br>

___

_END_