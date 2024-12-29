# -*- coding: utf-8 -*-
"""

美元計價-美元股票資產配置

1. 分配資產配置比例 
2. 取得相關資產資料
3. 資產配置風險報酬計算 
4. 資產配置權益曲線圖

"""

# 載入函數工具檔
from Data import getDataYF, getMultipleReturn
from FinancialMetrics import PortfolioRiskReturnRatio
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

# 取出低成本 股市ETF
url = "https://www.moneydj.com/etf/eb/ET305001list.djhtm?A=22&B=&C=4&D=&E=&F=&G=&H=&I=&J=&K=&L=&O=&P=&Q=&T=&U=&R=100&X=&Y=&EB=&order=3&SS=&CC=&st=&EFX=&AP=&Z=2&M=0&S=6"
response = requests.get(url)
df = pd.read_html(response.text)[0]
stock_df = df[(df["幣別"] == "美元") & (df["管理費(%)"] < 0.2)]
stock_list = stock_df["程式碼"].to_list()

# 抓到所有歷史報酬率
ret_dataframe = getMultipleReturn(getDataYF, ["UUP"] + stock_list, "adj close")
# 將商品程式碼換成商品名稱
stock_name_list = (stock_df["程式碼"] + stock_df["ETF名稱"]).to_list()
ret_dataframe.columns = ["UUP"] + stock_name_list

# 計算相關性
corr = round(ret_dataframe.corr(), 2)

# 並繪製熱力圖
plt.figure(figsize=(18, 14))
sns.heatmap(corr, cmap="Blues", annot=True)
plt.show()

# 股票美元資產配置比例
asset_allocation = {"UUP": 0.50, "BKIE": 0.50}

# 計算投資組合風險報酬
PortfolioRiskReturnRatio(getDataYF, asset_allocation, "adj close", 500000)
