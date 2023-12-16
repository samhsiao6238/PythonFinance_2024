# 載入必要的套件
import time,requests,os,datetime,random
from json import loads
import pandas as pd

# 切換工作路徑
os.chdir('調整為自己的存檔路徑')

c_datetime=datetime.datetime.now()
c_day=c_datetime.strftime('%Y%m%d')

first_write=True

while c_day>'20190101':
    
    c_datetime -= datetime.timedelta(1)
    c_day=c_datetime.strftime('%Y%m%d')

    print(c_day)
    url='https://www.twse.com.tw/exchangeReport/TWT93U?response=json&date='+c_day+'&_=1653293058208'
    
    
    html=requests.get(url)
    jsdata=loads(html.text)
    
    if 'data' not in jsdata.keys():
        print(c_day,'爬蟲失敗')
        continue        
    
    data=pd.DataFrame(jsdata['data'],columns=jsdata['fields'])
    data['日期']=c_day
    
    if first_write:
        data.to_csv('融券借券爬蟲資料.csv',encoding='cp950',index=False) 
        first_write=False
    else:
        data.to_csv('融券借券爬蟲資料.csv',encoding='cp950',mode='a',index=False,header=False) 

    
    # 隨機休息 5-10秒
    time.sleep(random.randint(5,10))
    
