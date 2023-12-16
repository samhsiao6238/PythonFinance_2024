# 載入必要套件
from Data import getTSEPriceAndMarginTrade
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='2618'
data=getTSEPriceAndMarginTrade(prod,'2019-01-01','2022-05-01')

# 融資融券餘額
data['融券今日餘額']=data['融券今日餘額'].astype(int)
data['融資今日餘額']=data['融資今日餘額'].astype(int)

# 計算券資比
data['券資比']=data['融券今日餘額']/data['融資今日餘額']

# 繪製副圖
addp=[]
# 融資融券
addp.append(mpf.make_addplot(data['融資今日餘額'],panel=1,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['融券今日餘額'],panel=2,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['券資比'],panel=3,color='red',secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp,v_enable=False)


