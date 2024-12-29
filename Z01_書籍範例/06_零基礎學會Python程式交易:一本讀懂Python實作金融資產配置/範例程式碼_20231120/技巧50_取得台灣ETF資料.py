# -*- coding: utf-8 -*-
"""

取得全台灣ETF商品標的

"""

# 載入函數工具檔
from Data import getDataFM
from FinMind.data import DataLoader

api = DataLoader()

# 取得全台灣ETF商品標的
stock_info = api.taiwan_stock_info()
ETF_group = stock_info[stock_info["industry_category"] == "ETF"]

# 取得ETF資料
prod = ETF_group[ETF_group["stock_name"] == "元大台灣50"]["stock_id"].iloc[0]
data = getDataFM(prod)

# 繪製ETF走勢圖
data["close"].plot()
