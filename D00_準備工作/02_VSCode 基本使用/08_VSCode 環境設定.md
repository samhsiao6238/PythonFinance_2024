# VSCode 環境設定

<br>

## 預設環境設置

1. 點擊左下角的齒輪可進入設定的介面操作。

    ![](images/img_30.png)

<br>

2. 可以輸入 `settings` 後開啟設定文件查看與編輯。

    ![](images/img_31.png)

<br>

## 自訂的設定

1. 先選定或建立一個專案資料夾如 `My Python`。

    ![](images/img_32.png)

<br>

2. 在根目錄建立一個 .vscode 資料夾。
    
    ![](images/img_33.png)

<br>

3. 在資料夾內建立一個 settings.json 設定檔案。

    ![](images/img_28.png)

<br>

## 常用設定

1. Flake8 長度限制。

    ```json
    {
        // flake8 長度
        "python.linting.flake8Args": ["--max-line-length", "200"]
    }
    ```

<br>

---

_END：持續補充_