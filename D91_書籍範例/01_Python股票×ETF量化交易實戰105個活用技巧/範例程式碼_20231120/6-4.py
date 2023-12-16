# 載入必要套件
from Data import getDataYF,getDataFM
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf
from talib.abstract import RSI

# 取得回測資料
prod='0050'
data=getDataFM(prod,'2007-01-01','2022-05-01')

# 計算相對強弱指標
data['rsi']=RSI(data,timeperiod=10)
                   
# 繪製副圖
addp=[]
addp.append(mpf.make_addplot(data['rsi'],panel=2,secondary_y=False))
addp.append(mpf.make_addplot([80]*len(data['rsi']),panel=2,secondary_y=False))
addp.append(mpf.make_addplot([40]*len(data['rsi']),panel=2,secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp)


