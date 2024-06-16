# -*- coding: utf-8 -*-
"""

美元股債資產配置(基礎)

1. 找出股債相關性
2. 分配資產配置比例 
3. 取得相關資產資料
4. 資產配置風險報酬計算 
5. 資產配置權益曲線圖
6. 尋找最好的股債比

"""

# 載入函數工具檔
from Data import getDataYF, getMultipleReturn
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

# 取出常見全世界債券ETF
url = "https://www.moneydj.com/etf/eb/ET305001list.djhtm?Z=2&S=6&M=0&N=&A=24&B=&C=&D=&E=&F=&G=&H=&I=&J=&K=&L=&O=&P=&Q=&T=&U=100&X=&Y=&EB=&order=4&SS=&CC=&st=&EFX=&AP=&R="
response = requests.get(url)
df = pd.read_html(response.text)[0]
bond_df = df[(df["幣別"] == "美元") & (df["管理費(%)"] < 0.1)]

bond_list = bond_df["程式碼"].to_list()

# 抓到所有歷史報酬率
ret_dataframe = getMultipleReturn(getDataYF, ["QQQ"] + bond_list, "adj close")
# 將商品程式碼換成商品名稱
bond_name_list = (bond_df["程式碼"] + bond_df["ETF名稱"]).to_list()
ret_dataframe.columns = ["QQQ"] + bond_name_list

# 計算相關性
corr = round(ret_dataframe.corr(), 2)

# 並繪製熱力圖
plt.figure(figsize=(18, 14))
sns.heatmap(corr, cmap="Blues", annot=True)
plt.show()

# 股債資產配置比例
asset_allocation = {"QQQ": 0.50, "IBTD": 0.50}

# 計算投資組合風險報酬
PortfolioRiskReturnRatio(getDataYF, asset_allocation, "adj close", 500000)
