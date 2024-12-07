# -*- coding: utf-8 -*-
"""

取得外匯商品資料

"""

# 載入函數工具檔
import requests
import pandas as pd
from Data import getDataYF
from bs4 import BeautifulSoup

# 取得外匯商品標的
url = "https://tw.stock.yahoo.com/currencies"
html = requests.get(url)
soup = BeautifulSoup(html.text)
ul = soup.find("ul", class_="M(0) P(0) List(n)")
rs = []
for li in ul.find_all("li"):
    tmplist = [i.text for i in li.find_all("span")]
    rs.append(tmplist)
currencies_info = pd.DataFrame(rs)

# 取得外匯資料
prod = currencies_info.iloc[0, 2]
data = getDataYF(prod)

# 繪製外匯走勢圖
data["close"].plot()
