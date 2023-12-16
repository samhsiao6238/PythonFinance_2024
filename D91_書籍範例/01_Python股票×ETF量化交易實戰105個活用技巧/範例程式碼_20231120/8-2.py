# 載入必要套件
from Data import getPriceAndInstInvest_TSE
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='0050'
data=getPriceAndInstInvest_TSE(prod,'2019-05-01','2022-05-01')

# 計算 外資平均買賣
data['F_day']=data['外陸資買進股數(不含外資自營商)']-data['外陸資賣出股數(不含外資自營商)']
data['F_month']=(data['F_day']).rolling(20).sum()
data['F_mean']=(data['F_month']).rolling(40).mean()

# 繪製副圖
addp=[]
# 外資買賣力道
addp.append(mpf.make_addplot(data['F_day'],panel=1,type='bar',secondary_y=False))
addp.append(mpf.make_addplot(data['F_month'],panel=1,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['F_mean'],panel=1,color='blue',secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp,v_enable=False)


