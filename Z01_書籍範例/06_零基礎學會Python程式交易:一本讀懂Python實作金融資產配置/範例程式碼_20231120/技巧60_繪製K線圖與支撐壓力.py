# -*- coding: utf-8 -*-
"""

繪製支撐與壓力

"""

# 載入函數工具檔
from Data import getDataFM
import mplfinance as mpf

# 取得資料
prod = "0050"
data = getDataFM(prod)

# 設定繪圖樣式
mcolor = mpf.make_marketcolors(up="r", down="g", inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style="yahoo", marketcolors=mcolor)

# 計算支撐與壓力
data["ceil"] = data.rolling(60)["close"].max()
data["floor"] = data.rolling(60)["close"].min()

# 繪製支撐與壓力
data = data.iloc[-200:].copy()
addp = []
addp.append(mpf.make_addplot(data["ceil"]))
addp.append(mpf.make_addplot(data["floor"]))
mpf.plot(data, type="candle", style=mstyle, addplot=addp)
