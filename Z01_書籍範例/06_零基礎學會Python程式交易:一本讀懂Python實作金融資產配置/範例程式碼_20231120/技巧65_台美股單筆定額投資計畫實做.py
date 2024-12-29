# -*- coding: utf-8 -*-
"""

單筆定額計算實務

"""

# 載入函數工具檔
from Data import getDataFM, getDataYF
from FinancialMetrics import RiskReturnRatio

# 取得台股資料
prod = "2330"
data = getDataFM(prod)

# 計算風險報酬評價函數
RiskReturnRatio(data, "adj close")

# 取得美股資料
prod = "AAPL"
data = getDataYF(prod)

# 計算風險報酬評價函數
RiskReturnRatio(data, "adj close")
