# 載入必要的套件
import time,requests,os,datetime,random
from json import loads
import pandas as pd

# 切換工作路徑
os.chdir('調整為自己的存檔路徑')

ym_list=[]
for y in range(2010,2023):
    for m in range(1,13):
        y=str(y)
        m=str(m).zfill(2)
        ym_list.append([y,m])

# 從 2010年開始爬蟲
first_write=True

for y,m in ym_list:
    ym=y+m
    try:
        print(ym)
        
        y = int(y)-1911
        m = int(m)
        
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_%s_%s_0.html'%(y,m)

        # 下載該年月的網站，並用 pandas 轉換成 dataframe
        r = requests.get(url)
        r.encoding = 'utf-8'
        # 解析成pd.Dataframe
        dfs = pd.read_html(r.text)
        
        # 取出欄位數量為11的表格
        data = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])

        # 調整欄位名稱
        if data.shape[1] == 10:
            data.columns=['公司代號','公司名稱','當月營收','上月營收','去年當月營收','上月比較增減(%)','去年同月增減(%)','當月累計營收','去年累計營收','前期比較增減(%)']
        else:
            data.columns=['公司代號','公司名稱','當月營收','上月營收','去年當月營收','上月比較增減(%)','去年同月增減(%)','當月累計營收','去年累計營收','前期比較增減(%)','備註']
        data['備註'] = ''
        data=data[data['公司代號'].str[-2:] != '合計']
        data['日期'] = ym+'10'
        
        if first_write:
            data.to_csv('月營收爬蟲資料.csv',encoding='utf-8',index=False)
            first_write=False
        else:
            data.to_csv('月營收爬蟲資料.csv',encoding='utf-8',mode='a',index=False,header=False) 
    except:
        print(ym ,'爬蟲失敗')
        continue
    finally:
        time.sleep(random.randint(1,5))









