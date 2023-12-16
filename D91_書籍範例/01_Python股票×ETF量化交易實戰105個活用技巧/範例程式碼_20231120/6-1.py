# 載入必要套件
from Data import getDataYF, getDataFM
from BackTest import ChartTrade, Performance
import pandas as pd
import mplfinance as mpf
from talib.abstract import SMA, WMA, EMA

# 取得回測資料
prod = "0050"
data = getDataFM(prod, "2007-01-01", "2023-05-")

# 計算指數移動平均線
data["ema"] = EMA(data, timeperiod=120)
data["wma"] = WMA(data, timeperiod=120)
data["sma"] = SMA(data, timeperiod=120)

# 繪製副圖
addp = []
addp.append(mpf.make_addplot(data["ema"]))
addp.append(mpf.make_addplot(data["wma"]))
addp.append(mpf.make_addplot(data["sma"]))

# 繪製K線圖與交易明細
ChartTrade(data, addp=addp)
