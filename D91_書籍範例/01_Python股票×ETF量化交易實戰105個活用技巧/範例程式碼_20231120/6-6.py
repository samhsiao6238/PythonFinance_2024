# 載入必要套件
from Data import getDataYF,getDataFM
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf
from talib.abstract import RSI

# 取得回測資料
prod='0050'
data=getDataFM(prod,'2007-01-01','2022-05-01')

# 計算相對強弱指標
data['rsi1']=RSI(data,timeperiod=120)
data['rsi2']=RSI(data,timeperiod=150)

# 初始部位
position=0
trade=pd.DataFrame()
# 開始回測
for i in range(data.shape[0]-1):
    # 取得策略會應用到的變數
    c_time=data.index[i]
    c_high=data.loc[c_time,'high']
    c_close=data.loc[c_time,'close']
    c_rsi1=data.loc[c_time,'rsi1']
    c_rsi2=data.loc[c_time,'rsi2']
    # 取下一期資料做為進場資料
    n_time=data.index[i+1]
    n_open=data.loc[n_time,'open']
    
    # 進場程序
    if position == 0 :
        if c_rsi1 > c_rsi2 :
            position = 1  
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
    # 出場程序
    elif position ==1 :
        # 出場邏輯
        if c_rsi1 < c_rsi2  * 0.999 :
            position = 0
            cover_time=n_time
            cover_price=n_open
            # 交易紀錄
            trade=trade.append(pd.Series([
                        prod,
                        'Buy',
                        order_time,
                        order_price,
                        cover_time,
                        cover_price,
                        order_unit
                    ]),ignore_index=True)

# 繪製副圖
addp=[]
addp.append(mpf.make_addplot(data['rsi1'],panel=2,secondary_y=False))
addp.append(mpf.make_addplot(data['rsi2'],panel=2,secondary_y=False))

# 績效分析
Performance(trade,'ETF')
# 繪製K線圖與交易明細
ChartTrade(data,trade,addp=addp)


