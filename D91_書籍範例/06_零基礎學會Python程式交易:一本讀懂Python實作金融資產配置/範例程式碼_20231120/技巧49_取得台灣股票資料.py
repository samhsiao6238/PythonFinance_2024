# -*- coding: utf-8 -*-
"""

取得全台灣股票商品標的

"""

# 載入函數工具檔
from Data import getDataFM
from FinMind.data import DataLoader

api = DataLoader()


# 取得全台灣股票商品標的
stock_info = api.taiwan_stock_info()
stock_group = stock_info[stock_info["industry_category"] == "半導體業"]

# 取得股票資料
prod = stock_group[stock_group["stock_name"] == "台積電"]["stock_id"].iloc[0]
data = getDataFM(prod)

# 繪製股票走勢圖
data["close"].plot()
