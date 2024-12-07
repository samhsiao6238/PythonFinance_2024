# -*- coding: utf-8 -*-
"""

多商品報酬曲線比較

"""

# 載入函數工具檔
from Data import getDataFM, getDataYF, getMultipleReturn

# 取得台股多商品資料 並繪製多商品報酬曲線圖
symbols = ["0050", "0056", "0051"]
all_price = getMultipleReturn(getDataFM, symbols, "adj close")
all_price.dropna().cumprod().plot()

# 取得美股多商品資料 並繪製多商品報酬曲線圖
symbols = ["AAPL", "AMZN", "TSLA"]
all_price = getMultipleReturn(getDataYF, symbols, "adj close")
all_price.dropna().cumprod().plot()
