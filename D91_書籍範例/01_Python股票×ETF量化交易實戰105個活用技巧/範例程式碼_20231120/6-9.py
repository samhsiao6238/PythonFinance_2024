# 載入必要套件
from Data import getDataYF,getDataFM
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf
from talib.abstract import EMA,ATR

# 取得回測資料
prod='0050'
data=getDataFM(prod,'2007-01-01','2022-05-01')

# 計算指數移動平均線
data['ema']=EMA(data,timeperiod=80)
data['atr1']=ATR(data,timeperiod=120)
data['atr2']=ATR(data,timeperiod=200)

# 繪製副圖
addp=[]
addp.append(mpf.make_addplot(data['ema']))
addp.append(mpf.make_addplot(data['atr1'],panel=2,secondary_y=False))
addp.append(mpf.make_addplot(data['atr2'],panel=2,secondary_y=False))

# 繪製K線圖與交易明細
ChartTrade(data,addp=addp)


