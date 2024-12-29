# pip 自動檢查版本出錯

_WARNING: There was an error checking the latest version of pip_

<br>

## 說明

1. 進行 pip 相關指令的時候出現以下警告。

    ![](images/img_12.png)

<br>

## 手動更新 pip

1. 命令。

    ```bash
    python -m pip install --upgrade pip
    ```

<br>

## 清除 pip 更新緩存

1. Linux。

    ```bash
    rm -r ~/.cache/pip/selfcheck/
    ```

<br>

2. macOS (OS X)。

    ```bash
    rm -r ~/Library/Caches/pip/selfcheck/
    ```

<br>

3. Windows (PowerShell)。

    ```powershell
    rm -r $env:LOCALAPPDATA\pip\cache\selfcheck\
    ```

<br>

## 強制重新安裝 pip

1. 命令。

    ```bash
    python -m pip install --upgrade --force-reinstall pip
    ```

<br>

___

_END_