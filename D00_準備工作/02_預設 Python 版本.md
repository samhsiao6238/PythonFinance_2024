# 預設版本

## Windows

1. 編輯系統環境變數。

    ![](images/img_05.png)

2. 點擊

    ![](images/img_06.png)

3. 系統變數

    ![](images/img_07.png)

4. 新增：設定完成務必逐一確認並且退出

    ![](images/img_08.png)

5. 重啟命令提示字元之後再次查詢，會發現預設版本變動了。

    ![](images/img_09.png)

6. 查詢版本

    ```bash
    python --version
    ```

    ![](images/img_10.png)

## MacOS

1. 編輯環境參數。

    ```bash
    sudo nano ~/.zshrc
    ```

2. 假設使用某個環境作為預設的版本。

    ```ini
    export PATH="/Users/samhsiao/Documents/PythonVenv/envDash/bin:$PATH"   
    ```
    
    ![](images/img_11.png)

3. 重新載入配置文件。

    ```bash
    source ~/.zshrc
    ```