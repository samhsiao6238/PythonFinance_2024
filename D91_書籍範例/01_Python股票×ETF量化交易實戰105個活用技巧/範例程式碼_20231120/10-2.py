# 載入必要套件
from Data import getTSEPriceAndRevenue
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='2618'
data=getTSEPriceAndRevenue(prod,'2010-01-01','2022-05-20')

# 繪製副圖
addp=[]
addp.append(mpf.make_addplot(data['去年同月增減(%)'],panel=1,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['前期比較增減(%)'],panel=2,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['當月營收'],panel=3,type='bar',color='red',secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp,v_enable=False)


