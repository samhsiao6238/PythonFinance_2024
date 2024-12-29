# -*- coding: utf-8 -*-
"""

台股資產配置

1. 分配資產配置比例 
2. 取得相關資產資料
3. 資產配置風險報酬計算 
4. 資產配置權益曲線圖

"""

# 載入函數工具檔
from Data import getDataFM
from FinancialMetrics import PortfolioRiskReturnRatio

# 定義資產配置商品、比例
# 台灣前50佔總市值的比例是佔67.62%
# 台灣中型100的比例是佔16.67%
# 共佔台灣總市值84.29%
asset_allocation = {"0050": 0.80, "0051": 0.20}

# 計算投資組合風險報酬
PortfolioRiskReturnRatio(getDataFM, asset_allocation, "adj close", 500000)
