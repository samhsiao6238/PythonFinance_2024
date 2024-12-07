# -*- coding: utf-8 -*-
"""

定期定額投資比較實作

"""
# 載入函數工具檔
from Data import getDataFM, getDataYF
from FinancialMetrics import MultipleReturnRegularFixedInvestment
import pandas as pd
import warnings

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# 計算台股定期定額報酬
MultipleReturnRegularFixedInvestment(
    getDataFM, ["0050", "0051", "0056"], "adj close", 20000
)

# 計算美股定期定額報酬
MultipleReturnRegularFixedInvestment(getDataYF, ["AAPL", "GOOG"], "adj close", 1000)
