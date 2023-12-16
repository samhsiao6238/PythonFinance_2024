"""
-----------------------
|  Python 每日訊號派送 |
-----------------------
"""

# 將歷史回測改為每日訊號派送程式流程
# 1. 將資料日期改為今日
# 2. 將回測資料運算至最後一天(不用取得t+1日，將不必要的程式碼刪除)
# 3. 每日狀態宣布
#     1維持空手(0)
#     2維持進場(1)
#     3進場訊號(0至1)
#     4出場訊號(1至0)


# 載入必要套件
from Data import getDataFM
from BackTest import ChartTrade,Performance,line_print
import pandas as pd
from talib.abstract import EMA
import mplfinance as mpf
import datetime

# 取得回測資料
prod='0050'
st='2010-01-01'
en=datetime.datetime.now().strftime('%Y-%m-%d')
data=getDataFM(prod,st,en)

# 計算指數移動平均線
data['ema']=EMA(data,timeperiod=120)

# 初始部位
position=0
# 當天訊號
signal=0
# 開始當日訊號派送
for i in range(1,data.shape[0]):
    # 取得策略會應用到的變數 
    c_time=data.index[i]
    c_close=data.loc[c_time,'close']
    c_ema=data.loc[c_time,'ema']
    
    # 進場程序
    if position == 0:
        # 進場邏輯 
        if c_close > c_ema*1.01 :
            position = 1
            signal=3
        else:
            signal=1
            
    # 出場程序
    elif position == 1:
        # 出場邏輯
        if c_close < c_ema*0.995 :
            position = 0
            signal=4
        else:
            signal=2
            

strategy_name='均線策略'
if signal==1:
    line_print('%s \n %s \n %s \n維持空手'%(strategy_name,prod,en))
elif signal==2:
    line_print('%s \n %s \n %s \n維持進場'%(strategy_name,prod,en))
elif signal==3:
    line_print('%s \n %s \n %s \n進場訊號'%(strategy_name,prod,en))
elif signal==4:
    line_print('%s \n %s \n %s \n出場訊號'%(strategy_name,prod,en))
