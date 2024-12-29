# -*- coding: utf-8 -*-
"""

取得原物料期貨商品資料

"""

# 載入函數工具檔
import pandas as pd
import requests
from Data import getDataYF
from bs4 import BeautifulSoup

# 取得原物料期貨商品標的
url = "https://tw.stock.yahoo.com/commodities"
html = requests.get(url)
soup = BeautifulSoup(html.text)
ul = soup.find("ul", class_="M(0) P(0) List(n)")
rs = []
for li in ul.find_all("li"):
    tmplist = [i.text for i in li.find_all("span")]
    rs.append(tmplist)
commodities_info = pd.DataFrame(rs)

# 取得原物料期貨資料
prod = commodities_info.iloc[0, 2]
data = getDataYF(prod)

# 繪製原物料期貨走勢圖
data["close"].plot()
