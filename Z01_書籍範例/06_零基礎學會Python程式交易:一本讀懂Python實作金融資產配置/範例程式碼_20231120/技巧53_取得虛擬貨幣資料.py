# -*- coding: utf-8 -*-
"""

取得虛擬貨幣商品資料

"""

# 載入函數工具檔
import pandas as pd
import requests
from Data import getDataYF
from bs4 import BeautifulSoup

# 取得虛擬貨幣商品標的
url = "https://tw.stock.yahoo.com/cryptocurrencies"
html = requests.get(url)
soup = BeautifulSoup(html.text)
ul = soup.find("ul", class_="M(0) P(0) List(n)")
rs = []
for li in ul.find_all("li"):
    tmplist = [i.text for i in li.find_all("span")]
    rs.append(tmplist)
crypto_info = pd.DataFrame(rs)

# 取得虛擬貨幣資料
prod = crypto_info.iloc[0, 2]
data = getDataYF(prod)

# 繪製虛擬貨幣走勢圖
data["close"].plot()
