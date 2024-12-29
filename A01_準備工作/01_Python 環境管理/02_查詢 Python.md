# 查詢當前 Python 環境

_Python 需要正確的版本以建立虛擬環境_

<br>

## 說明

1. 在 Windows11 的 CMD 中執行 `python` 指令，將會觸發啟動商店，不用理會。

    ![](images/img_31.png)

<br>

## Windows

1. 查詢當前 Python 版本。

    ```bash
    python --version
    ```

<br>

2. 查詢所有安裝的 Python 版本：請注意參數是數字的 `0`，`py` 是一個 Windows 平台特有的 Python 啟動器，用於管理和切換不同的 Python 版本。

    ```bash
    py -0
    ```

    ![](images/img_03.png)

<br>

3. 搜索並顯示所有在環境參數的系統路徑（System PATH）與 python 匹配的可執行文件路徑。

    ```bash
    where python
    ```
    
    ![](images/img_02.png)

<br>

4. 特別說明，在 Windows 系統中的 `AppData\Local\Microsoft\WindowsApps` 目錄中出現對應的執行檔通常是捷徑或佔位符，而不是真正的可執行檔，而這個檔案通常來自於透過 Microsoft Store 安裝 Python 時，`WindowsApps` 目錄會包含一個指向 Microsoft Store 安裝版本的 Python 捷徑。如果這個 Python 版本未被完整安裝或已被卸載，但捷徑未被刪除時，則試圖執行這個捷徑將不會有任何輸出，結果如下。

    ![](images/img_40.png)

<br>

## MacOS

1. 查詢當前 Python 版本。

    ```bash
    python --version
    ```

<br>

2. 查詢安裝路徑：返回在 PATH 環境變數中找到的第一個名為 python 的可執行文件的路徑。

    ```bash
    which python
    ```

    ![](images/img_04.png)

<br>

3. 查詢安裝路徑：列出所有在 PATH 環境變數中找到的匹配文件的路徑。

    ```bash
    which -a python3
    ```

    ![](images/img_15.png)

<br>

4. 若查詢 `Python`。

    ```bash
    which -a python
    ```

    ![](images/img_16.png)

5. 搜索標準系統目錄中所安裝的 Python。

    ```bash
    whereis python
    ```

<br>


---

_END_


