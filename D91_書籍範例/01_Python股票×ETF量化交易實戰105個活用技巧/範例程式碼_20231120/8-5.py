# 載入必要套件
from Data import getPriceAndInstInvest_FM
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='0050'
data=getPriceAndInstInvest_FM(prod,'2019-05-01','2022-05-01')

# 計算 外資平均買賣
data['F_day']=data['外陸資買進股數(不含外資自營商)']-data['外陸資賣出股數(不含外資自營商)']
data['F_month']=(data['F_day']).rolling(40).sum()
data['F_mean']=(data['F_month']).rolling(20).mean()

# 初始部位
position=0
trade=pd.DataFrame()
# 開始回測
for i in range(data.shape[0]-1):
    # 取得策略會應用到的變數
    c_time=data.index[i]
    c_high=data.loc[c_time,'high']
    c_close=data.loc[c_time,'close']
    c_F_month=data.loc[c_time,'F_month']
    c_F_mean=data.loc[c_time,'F_mean']
    # 取下一期資料做為進場資料
    n_time=data.index[i+1]
    n_open=data.loc[n_time,'open']
    
    # 進場程序
    if position == 0 :
        if c_F_month > c_F_mean :
            position = 1  
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
    # 出場程序
    elif position ==1 :
        # 出場邏輯
        if c_F_month < c_F_mean :
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
# 外資買賣力道
addp.append(mpf.make_addplot(data['F_month'],panel=1,color='red',secondary_y=False))
addp.append(mpf.make_addplot(data['F_mean'],panel=1,color='blue',secondary_y=False))

# 績效分析
Performance(trade,'ETF')
# 繪製K線圖與交易明細
ChartTrade(data,trade,addp=addp,v_enable=False)



