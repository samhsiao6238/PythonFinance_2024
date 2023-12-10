# 預設版本

_設置預設版本，僅供基礎了解使用，之後會透過虛擬環境來隔離開發環境的版本。_

<br>

## Windows

_Windows 系統裝機並未自帶 Python，這裡先忽略這件事，單就如何指定預設版本這個主題說明。_

<br>

1. 編輯系統環境變數。

    ![](images/img_05.png)

<br>

2. 點擊 `環境變數`。

    ![](images/img_06.png)

<br>

3. 在 `系統變數` 區塊點擊 `新增` 。

    ![](images/img_07.png)

<br>

4. 進行新增：設定完成務必逐一確認並且退出。

    _變數名稱_
    ```ini
    PY_PYTHON
    ```
    _變數值_
    ```ini
    3.9
    ```

    ![](images/img_08.png)

<br>

5. 重啟命令提示字元，輸入指令 `py` 再次查詢，可看到預設版本已經變更為 `3.9.13` 了。

    ![](images/img_09.png)

<br>

6. 查詢版本。

    ```bash
    python --version
    ```

    ![](images/img_10.png)

<br>

## MacOS

1. 編輯環境參數。

    ```bash
    sudo nano ~/.zshrc
    ```

<br>

2. 假設使用某個環境作為預設的版本。

    ```ini
    export PATH="/Users/samhsiao/Documents/PythonVenv/envDash/bin:$PATH"   
    ```
    
    ![](images/img_11.png)

<br>

3. 重新載入配置文件。

    ```bash
    source ~/.zshrc
    ```


<br>

---

_END_