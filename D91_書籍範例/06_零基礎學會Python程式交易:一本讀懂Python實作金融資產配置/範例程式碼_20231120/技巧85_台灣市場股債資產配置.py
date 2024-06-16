# -*- coding: utf-8 -*-
"""

台灣股債資產配置(基礎)

1. 找出股債相關性
2. 分配資產配置比例 
3. 取得相關資產資料
4. 資產配置風險報酬計算 
5. 資產配置權益曲線圖
6. 尋找最好的股債比

"""

# 載入函數工具檔
from Data import getDataFM, getMultipleReturn
from FinancialMetrics import PortfolioRiskReturnRatio
import seaborn as sns
from FinMind.data import DataLoader
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False
api = DataLoader()

# 取出台灣股市 債市 ETF
df = api.taiwan_stock_info()
bond_dataframe = df[
    (df["stock_id"].str[-1] == "B")
    & (df["stock_name"].str.contains("債"))
    & (df["stock_name"].str.contains("元大"))
]
ETF_dataframe = df[
    (df["industry_category"].str[:3] == "ETF")
    & (df["stock_name"].str.contains("元大"))
    & (df["stock_id"].str[-1].str.isnumeric())
]

ETF_list = ETF_dataframe["stock_id"].to_list()
bond_list = bond_dataframe["stock_id"].to_list()

# 抓到所有歷史報酬率
ret_dataframe = getMultipleReturn(getDataFM, ETF_list + bond_list, "adj close")
# 將商品程式碼換成商品名稱
ETF_name_list = (ETF_dataframe["stock_id"] + ETF_dataframe["stock_name"]).to_list()
bond_name_list = (bond_dataframe["stock_id"] + bond_dataframe["stock_name"]).to_list()
ret_dataframe.columns = ETF_name_list + bond_name_list

# 計算相關性
corr = round(ret_dataframe.corr(), 2)

# 並繪製熱力圖
plt.figure(figsize=(18, 14))
sns.heatmap(corr, cmap="Blues", annot=True)
plt.show()

# 股債資產配置比例
asset_allocation = {"0050": 0.50, "00719B": 0.50}

# 計算投資組合風險報酬
PortfolioRiskReturnRatio(getDataFM, asset_allocation, "adj close", 500000)
