# -*- coding: utf-8 -*-
"""

繪製金融圖表

https://pypi.org/project/mplfinance/

pip install mplfinance
"""

# 載入函數工具檔
import pandas as pd
from Data import getDataYF, getDataFM
import mplfinance as mpf

# 取得資料
prod = "^GSPC"
data = getDataYF(prod)
data = data.iloc[-10:]

# 繪製圖表
mpf.plot(data)

# 繪製K線圖
mpf.plot(data, type="candle")

# 查看樣式
mpf.available_styles()

# 調整樣式
mpf.plot(data, type="candle", style="yahoo")

# 修改K線顏色
mcolor = mpf.make_marketcolors(up="r", down="g", inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style="yahoo", marketcolors=mcolor)
mpf.plot(data, type="candle", style=mstyle)
