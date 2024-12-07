# -*- coding: utf-8 -*-
"""

取得海外股票商品資料

"""

# 載入函數工具檔
from Data import getDataYF
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 取得海外股票商品標的
# 美股商品網址 https://tw.stock.yahoo.com/us-market
# 港股商品網址 https://tw.stock.yahoo.com/hk-market
# 滬深股商品網址 https://tw.stock.yahoo.com/cn-market
url = "https://tw.stock.yahoo.com/cn-market"
html = requests.get(url)
soup = BeautifulSoup(html.text)
ul = soup.find("ul", class_="M(0) P(0) List(n)")
rs = []
for li in ul.find_all("li"):
    tmplist = [i.text for i in li.find_all("span")]
    rs.append(tmplist)
stock_info = pd.DataFrame(rs)

# 取得股票資料
prod = stock_info.iloc[0, 1]
data = getDataYF(prod)

# 繪製股票走勢圖
data["close"].plot()
data["adj close"].plot()
