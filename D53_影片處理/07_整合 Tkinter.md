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

___

_END_