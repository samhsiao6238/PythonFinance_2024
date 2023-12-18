# -*- coding: utf-8 -*-
"""

金融歷史資料套件應用
yahoo finance ：金融商品資料取得

安裝套件
# pip install yfinance 

"""

# 載入套件
import yfinance as yf

# 商品名稱
prod = "^GSPC"

# 取得歷史資料
data = yf.download(prod, start="2017-01-01", end="2017-04-30")

# 取得全部資料
data = yf.download(prod, period="max")
