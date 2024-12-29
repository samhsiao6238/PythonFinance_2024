# -*- coding: utf-8 -*-
"""

永久投資組合

"""

# 載入函數工具檔
from Data import getDataYF, getMultipleReturn
from FinancialMetrics import PortfolioRiskReturnRatio

# 定義資產配置商品、比例
asset_allocation = {
    "VTI": 0.25,  # 股票 25%
    "TLT": 0.25,  # 長期債券 25%
    "SHY": 0.25,  # 現金選擇 25%
    "GLD": 0.25,  # 貴金屬 25%
}

# 計算投資組合風險報酬
PortfolioRiskReturnRatio(getDataYF, asset_allocation, "adj close", 500000)
