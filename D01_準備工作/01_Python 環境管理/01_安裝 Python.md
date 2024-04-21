# 安裝 Python

_前往 [官網](https://www.python.org/) 進行安裝_

<br>

## Windows

1. 在下載的頁籤中選擇 Windows。

    ![](images/img_32.png)

<br>

2. 官網 [下載](https://www.python.org/downloads/windows/) 。

    ![](images/img_21.png)

<br>

3. 以系統管理員身份執行安裝。

    ![](images/img_22.png)

<br>

4. 務必勾選添加路徑，然後選擇客製化安裝。

    ![](images/img_23.png)

<br>

5. 點擊 `NEXT` 。

    ![](images/img_24.png)

<br>

6. 勾選 `Install for all users`，就是因為要在這裡確認 `路徑中沒有中文`，所以選擇客製化安裝。

    ![](images/img_25.png)

<br>

7. 安裝完成，關閉即可。

    ![](images/img_26.png)

<br>

8. 也可以允許長檔名。 

    ![](images/img_48.png)

<br>

_回到終端機_

9. 查詢版本。

    ```bash
    python --version
    ```

<br>

10. 就會是剛剛安裝完成的版本。

    ![](images/img_27.png)


<br>

## MacOS
_相同部分不贅述_

<br>

1. [官方下載](https://www.python.org/downloads/macos/) 。

    ![](images/img_14.png)

<br>

2. 接著就是繼續、繼續、同意、安裝、密碼

    ![](images/img_33.png)

<br>

3. 安裝完成會在 Applications 中看到。

    ![](images/img_34.png)

<br>

4. 特別注意，在 MacOS 中安裝了不同版本的 Python 後，系統並不會修正環境參數檔案如 `.zshrc` 的內容，但是會自動更新 `/usr/local/bin` 中的符號鏈接，也就是將新安裝的版本指向 Python 與 Python3，所以查詢版本時會發現已經變更為最新安裝的版本。

<br>

---

_END_