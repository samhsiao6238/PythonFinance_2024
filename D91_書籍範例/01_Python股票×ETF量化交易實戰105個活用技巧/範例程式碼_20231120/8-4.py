# 載入必要套件
from Data import getPriceAndInstInvest_TSE
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='0050'
data=getPriceAndInstInvest_TSE(prod,'2019-05-01','2022-05-01')

# 計算 投信平均買賣
data['D_day']=data['自營商買進股數(自行買賣)']-data['自營商賣出股數(自行買賣)']
data['D_month']=(data['D_day']).rolling(20).sum()
data['D_mean']=(data['D_month']).rolling(60).mean()

# 繪製副圖
addp=[]
# 外資買賣力道
addp.append(mpf.make_addplot(data['D_day'],panel=1,type='bar',secondary_y=False))
addp.append(mpf.make_addplot(data['D_month'],panel=1,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['D_mean'],panel=1,color='blue',secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp,v_enable=False)


