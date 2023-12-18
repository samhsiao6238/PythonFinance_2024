# -*- coding: utf-8 -*-
"""

取得全世界指數商品

"""

# 載入函數工具檔
from Data import getDataYF
import requests
import pandas as pd

# 取得全世界指數商品標的
url = "https://finance.yahoo.com/world-indices"
html = requests.get(url)
web_data = pd.read_html(html.text)[0]

# 取得第一個指數商品資料
prod = web_data["Symbol"][0]
data = getDataYF(prod)

# 繪製指數走勢圖
data["close"].plot()
