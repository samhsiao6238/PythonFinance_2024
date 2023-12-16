# 載入必要套件
from Data import getTSEPriceAndShortSales
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='2618'
data=getTSEPriceAndShortSales(prod,'2019-01-01','2022-05-01')

# 融券借券餘額
data['融券今日餘額']=data['融券今日餘額'].astype(int)
data['借券當日餘額']=data['借券當日餘額'].astype(int)

# 繪製副圖
addp=[]
# 融券借券
addp.append(mpf.make_addplot(data['融券今日餘額'],panel=1,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['借券當日餘額'],panel=2,color='red',secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp,v_enable=False)
