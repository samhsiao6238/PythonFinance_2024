# -*- coding: utf-8 -*-
"""

金融歷史資料套件應用
finmind ：國內金融產品資料取得

# pip install FinMind 

"""

# 載入套件
from FinMind.data import DataLoader

api = DataLoader()

# 載入商品名稱
symbol = "2330"

# 取得歷史資料
data = api.taiwan_stock_daily_adj(
    stock_id=symbol, start_date="1900-01-01", end_date="2023-01-01"
)
