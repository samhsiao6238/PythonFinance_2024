# -*- coding: utf-8 -*-
"""

取得海外ETF商品資料

"""

# 載入函數工具檔
from Data import getDataYF
import pandas as pd

# 取得海外ETF商品標的
url = "https://www.moneydj.com/etf/x/rank/rank0004.xdjhtm?erank=mkt&eord=t150032"
web_data = pd.read_html(url)
ETF_info = web_data[1]
ETF_info_vanguard = ETF_info[ETF_info["ETF名稱"].str.contains("Vanguard")]

# 取得海外ETF資料
prod = ETF_info_vanguard.loc[1, "程式碼"]
data = getDataYF(prod)

# 繪製海外ETF走勢圖
data["close"].plot()
