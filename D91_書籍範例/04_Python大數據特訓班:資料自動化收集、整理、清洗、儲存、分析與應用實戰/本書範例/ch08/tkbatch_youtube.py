def clickDown():  #按「下載影片」鈕後處理函式
    global getvideo
    
    labelMsg.config(text="")  #清除提示訊息
    if(url.get()==""):  #若未輸入網址就顯示提示訊息
        labelMsg.config(text="網址欄位必須輸入！")
    else:
        urlin = url.get()
    if(path.get()==""):
        pathdir = 'download'
    else:
        pathdir = path.get()
        pathdir = pathdir.replace("\\", "\\\\")  #將「\」轉換為「\\」
    
    playlist = Playlist(urlin)  #建立物件  
    videolist = playlist.video_urls  #取得所有影片連結
    
    pathdir = 'download'  #下載資料夾
    n = 1
    for video in videolist:
        yt = YouTube(video)
        yt.streams.filter(subtype='mp4', res=getvideo, progressive=True).first().download(pathdir)  #下載mp4影片
        n = n + 1
    labelMsg.config(text="下載完成！")
    
def rbVideo():  #點選選項按鈕後處理函式
    global getvideo
    getvideo = videorb.get()
    
from pytube import YouTube
from pytube import Playlist
import tkinter as tk

win=tk.Tk()
win.geometry("530x280")  #設定主視窗解析度
win.title("下載Youtube影片")
getvideo = "360p"  #影片格式
videorb = tk.StringVar()  #選項按鈕值
url = tk.StringVar()  #影片網址
path = tk.StringVar()  #存檔資料夾

label1=tk.Label(win, text="Youtube網址：")
label1.place(x=123, y=30)
entryUrl = tk.Entry(win, textvariable=url)
entryUrl.config(width=40)
entryUrl.place(x=220, y=30)

label2=tk.Label(win, text="存檔路徑(預設為download資料夾)：")
label2.place(x=10, y=70)
entryPath = tk.Entry(win, textvariable=path)
entryPath.config(width=40)
entryPath.place(x=220, y=70)

btnDown = tk.Button(win, text="下載影片", command=clickDown)
btnDown.place(x=200, y=110)

rb1 = tk.Radiobutton(win, text='360p, mp4', variable=videorb, value='360p', command=rbVideo)
rb1.place(x=200, y=150)
rb1.select()
rb2 = tk.Radiobutton(win, text='720p, mp4', variable=videorb, value='720p', command=rbVideo)
rb2.place(x=200, y=180)

labelMsg = tk.Label(win, text="", fg="red")  #訊息標籤
labelMsg.place(x=200, y=220)
    
win.mainloop()
