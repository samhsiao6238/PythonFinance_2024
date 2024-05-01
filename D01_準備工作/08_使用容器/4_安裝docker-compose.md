# 安裝 `docker-compose` 

_[官方文件中](https://docs.docker.com/compose/install/) 依據作業系統分為 Windows、MacOS 和 Linux 三個安裝指南 。_

<br>

## MacOS

### 安裝

1. 建議使用 `Docker Desktop`，因為 `docker-compose` 已經包含在內而不需要單獨安裝。

<br>

2. 如果要單獨安裝或更新 `docker-compose`，可以透過 Homebrew 安裝。

<br>

3. 指令。

    ```bash
    # 安裝
    brew install docker-compose
    # 更新
    brew upgrade docker-compose
    ```

<br>

### 解除安裝 

1. 解除安裝。

    ```bash
    brew uninstall docker-compose
    ```

<br>

2. 檢查是否有遺留的文件。

    ```bash
    which docker-compose
    ```

<br>

3. 假如還有遺留的文件則進行刪除。 

    ```bash
    sudo rm $(which docker-compose)
    ```

<br>

4. 清理 Homebrew 的緩存。

    ```bash
    brew cleanup
    ```

<br>

5. 檢查是否有相關的設置文件。

    ```bash
    ls ~/.docker
    ```

<br>

6. 假如資料夾內有跟 `docker-compose` 相關的文件則刪除。

    ```bash
    rm -rf ~/.docker/<前一個步驟找到的文件>
    ```

<br>

### 安裝完畢檢查狀態
1. 查看內容是否為一個有效的二進位文件。

    ```bash
    cat /usr/local/bin/docker-compose
    ```

2. 確認路徑是否在 `/opt/homebrew/bin/`，假如不是的話務必確保路徑已寫入 `.zshrc`。

    ```bash
    which docker-compose
    ```

<br>

3. 假如文件正確位於 `/opt/homebrew/bin/`，請確認路徑是否已經寫入。

    ```bash
    echo $PATH
    ```

<br>

4. 假如未寫入 PATH 中，請在 `.zshrc` 中添加以下語句。

    ```bash
    export PATH="/opt/homebrew/bin:$PATH"
    ```

<br>

5. 加載設定文件。

    ```bash
    source ~/.zshrc
    ```

<br>

6. 如果問題依舊存在，可嘗試重新鏈接。

    ```bash
    brew unlink docker-compose && brew link docker-compose
    ```

<br>

## Windows

1. 建議使用 `Docker Desktop for Windows`，同樣包含了 `docker-compose`。

<br>

2. 如果需要單獨安裝，可從 GitHub [下載](https://github.com/docker/compose/releases) `docker-compose` 的 Windows 版本的二進位。

<br>

3. 將下載的檔案放到 Docker 安裝目錄下的 `bin` 資料夾中，通常是 `C:\Program Files\Docker\Docker\resources\bin`。

<br>

4. 確保這個目錄在您的系統 PATH 環境變數中。

<br>

## Linux

_使用以下步驟安裝 `docker-compose`_

<br>

1. 使用 `curl` 指令從 GitHub 發布頁下載最新的 `docker-compose` 執行檔到 `/usr/local/bin/docker-compose`，請替換下面指令中的 <v2.x.x> 為最新版本號。

    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.x.x/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/ bin/docker-compose
    ```

<br>

2. 更改下載的檔案的權限，使其成為可執行檔。

    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```

<br>

3. 檢查 `docker-compose` 版本以確保正確安裝。

    ```bash
    docker-compose --version
    ```

<br>

___

_END_