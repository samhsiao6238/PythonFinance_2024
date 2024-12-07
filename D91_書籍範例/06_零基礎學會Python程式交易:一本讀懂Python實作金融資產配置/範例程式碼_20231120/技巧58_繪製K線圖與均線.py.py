# -*- coding: utf-8 -*-
"""

繪製移動平均線

"""

# 載入函數工具檔
from Data import getDataYF
import mplfinance as mpf

# 設定繪圖樣式
mcolor = mpf.make_marketcolors(up="r", down="g", inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style="yahoo", marketcolors=mcolor)

# 取得資料
prod = "AAPL"
data = getDataYF(prod)

# 計算移動平均線
data["5ma"] = data.rolling(5)["close"].mean()
data["20ma"] = data.rolling(20)["close"].mean()
data["60ma"] = data.rolling(60)["close"].mean()

# 繪製移動平均線
data = data.iloc[-200:].copy()
addp = []
addp.append(mpf.make_addplot(data["5ma"]))
addp.append(mpf.make_addplot(data["20ma"]))
addp.append(mpf.make_addplot(data["60ma"]))
mpf.plot(data, type="candle", style=mstyle, addplot=addp)
