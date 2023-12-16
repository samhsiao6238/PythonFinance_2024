# 載入必要套件
from Data import getDataYF,getDataFM
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf
from talib.abstract import MACD

# 取得回測資料
prod='0050'
data=getDataFM(prod,'2007-01-01','2022-05-01')

# 計算MACD
data=data.join(MACD(data,40,120,60))
                   
# 繪製副圖
addp=[]
addp.append(mpf.make_addplot(data['macdhist'],type='bar',panel=2,secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp)


