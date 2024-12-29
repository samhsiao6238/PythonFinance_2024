# 整合 Tkinter

_使用圖形介面下載影片_

<br>

## 步驟

1. 建立腳本 `app.py`，並寫入以下代碼。

    ```python
    from tkinter import *
    from yt_dlp import YoutubeDL


    def download_video():
        url = url_entry.get()
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.config(text="下載完成！")

    window = Tk()
    window.title("YouTube 影片下載器")

    url_label = Label(window, text="影片網址：")
    url_label.grid(row=0, column=0)
    url_entry = Entry(window, width=40)
    url_entry.grid(row=0, column=1)

    download_button = Button(
        window, text="下載", command=download_video
    )
    download_button.grid(row=1, column=0, columnspan=2)

    status_label = Label(window, text="")
    status_label.grid(row=2, column=0, columnspan=2)

    window.mainloop()
    ```

<br>

2. 運行腳本。

    ```bash
    python app.py
    ```

<br>

3. 運行後跳出視窗，其中警告 Python 應用程序 app.py 在使用 MacOS 的 GUI 系統tkinter 時，嘗試利用 MacOS 的應用程序狀態恢復功能，但沒有啟用安全編碼功能；這個警告不影響應用程序功能，可選擇忽略它。

    <img src="images/img_04.png" width="400px">

<br>

## 補充說明

_一般來說，使用 `from module import *` 這種方式是不推薦的，因為它會將模組中的所有函數、類、變數等直接導入到當前的命名空間，主要的缺點如下。_

<br>

1. 名稱衝突：導入所有名稱會增加名稱衝突的風險，特別是需要使用多個模組時。

<br>

2. 代碼可讀性較差，讀者無法立即反應某個名稱是來自哪個模組，特別是當腳本很長或引用很多外部模組時。

<br>

3. 因為在部分 IDE 工具中必須能推測代碼中的名稱來源以便進行自動補全功能和代碼分析，所以這樣的導入將不利於開發工作。

<br>

## 在 `tkinter` 中常見 `from tkinter import *`

_主要原因有以下幾點_

<br>

1. `tkinter` 是一個 GUI 工具包，使用者需要頻繁調用大量小部件如 `Button`、`Label`、`Entry` 等，以及常量如 `LEFT`、`RIGHT`、`TOP`、`BOTTOM` 等；使用 `from tkinter import *` 可讓代碼更加簡潔，避免每次都需要加上 `tkinter.` 前綴。

<br>

2. `tkinter` 的名稱空間相對於其他模組較封閉，不容易與其他常用模組的名稱發生衝突，因此實際應用中名稱衝突的風險相對較小，所以這樣的用法成為一種可接受的模式。

<br>

3. 可使用較為折衷的寫法如下。

    ```python
    import tkinter as tk

    root = tk.Tk()
    button = tk.Button(root, text="Click Me")
    button.pack()
    root.mainloop()
    ```

<br>

___

_END_