# VSCode 環境設定

<br>

## 說明

1. 在根目錄建立一個 .vscode 資料夾。
2. 在資料夾內建立一個 settings.json 設定檔案。

    ![](images/img_28.png)

<br>

## 各項設定

1. Flake8 長度限制。

    ```json
    {
        // flake8 長度
        "python.linting.flake8Args": ["--max-line-length", "200"]
    }
    ```

<br>

---

_END_