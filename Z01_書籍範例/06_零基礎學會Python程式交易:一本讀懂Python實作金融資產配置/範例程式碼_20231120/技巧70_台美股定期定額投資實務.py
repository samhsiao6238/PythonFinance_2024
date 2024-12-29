# -*- coding: utf-8 -*-
"""

定期定額投資實作

pip install numpy_financial

"""

# 載入函數工具檔
from Data import getDataFM, getDataYF
from FinancialMetrics import ReturnRegularFixedInvestment

# 計算台股定期定額報酬
ReturnRegularFixedInvestment(getDataFM, "0050", "adj close", 20000)

# 計算美股定期定額報酬
ReturnRegularFixedInvestment(getDataYF, "AAPL", "adj close", 1000)
