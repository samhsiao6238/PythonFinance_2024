# -*- coding: utf-8 -*-
"""

全天候資產配置

"""


# 載入函數工具檔
from Data import getDataYF, getMultipleReturn
from FinancialMetrics import PortfolioRiskReturnRatio

# 定義資產配置商品、比例
asset_allocation = {
    "VTI": 0.3,  # 股票 30%
    "TLT": 0.40,  # 長期債券 40%
    "IEF": 0.15,  # 中期債券 15%
    "DBC": 0.075,  # 原物料 7.5%
    "GLD": 0.075,  # 貴金屬 7.5%
}


# 計算投資組合風險報酬
PortfolioRiskReturnRatio(getDataYF, asset_allocation, "adj close", 500000)
