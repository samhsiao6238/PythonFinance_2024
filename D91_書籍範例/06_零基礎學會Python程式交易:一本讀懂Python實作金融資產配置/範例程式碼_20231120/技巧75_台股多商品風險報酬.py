# -*- coding: utf-8 -*-
"""

(台灣)多金融商品比較

1. 取得台灣商品
2. 計算報酬、風險
3. 繪製在點圖上 X軸為風險 Y軸為報酬

"""

# 載入函數工具檔
from Data import getDataFM, getMultipleReturn
import pandas as pd
from FinMind.data import DataLoader
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False
api = DataLoader()

# 取出台灣元大投信的股票市場ETF
df = api.taiwan_stock_info()
ETF_dataframe = df[
    (df["industry_category"].str[:3] == "ETF")
    & (df["stock_name"].str.contains("元大"))
    & (df["stock_id"].str[-1].str.isnumeric())
]
stock_symbols = ETF_dataframe["stock_id"].to_list()

# 抓到所有歷史報酬率
ret_dataframe = getMultipleReturn(getDataFM, stock_symbols, "adj close")

# 風險報酬計算
rs = []
for col in ret_dataframe.columns:
    returns = ret_dataframe[col].dropna()
    if (returns.count() / 252) > 5:
        symbol_name = ETF_dataframe.loc[
            ETF_dataframe["stock_id"] == col, "stock_name"
        ].iloc[0]
        print(col)
        # 計算年化報酬率 年化標準差
        ann_ret = (returns).prod() ** (252 / returns.count()) - 1
        ann_risk = (returns - 1).std() * (252**0.5)
        ann_sharp = ann_ret / ann_risk
        print(f"{col}_{symbol_name}", returns.count())
        rs.append([f"{col}_{symbol_name}", ann_ret, ann_risk, ann_sharp])
# 每檔商品的風險報酬
rsdf = pd.DataFrame(rs)
rsdf.columns = ["名稱", "年化報酬", "年化風險", "夏普比率"]
rsdf.set_index("名稱", inplace=True)

ax = rsdf.plot.scatter(x="年化風險", y="年化報酬", c="夏普比率", colormap="viridis")

for i, txt in enumerate(rsdf.transpose()):
    ax.annotate(txt, (rsdf["年化風險"].iat[i] + 0.01, rsdf["年化報酬"].iat[i]))
