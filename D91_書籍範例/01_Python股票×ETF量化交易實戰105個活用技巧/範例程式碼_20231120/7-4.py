# 載入必要套件
from Data import getPriceAndShareHolder
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='0050'
data=getPriceAndShareHolder(prod,'2007-01-01','2022-05-01')

# 30張持有以下稱為散戶
data['minority']=data['1']+data['2']+data['3']+data['4']

# 算出過去的平均
data['minority_ma']=data.rolling(8)['minority'].mean()
data['ma']=data.rolling(4)['close'].mean()
data['total_people_ma']=data.rolling(8)['total_people'].mean()

# 初始部位
position=0
trade=pd.DataFrame()
# 開始回測
for i in range(data.shape[0]-1):
    # 取得策略會應用到的變數
    c_time=data.index[i]
    c_high=data.loc[c_time,'high']
    c_close=data.loc[c_time,'close']
    c_ma=data.loc[c_time,'ma']
    c_minority=data.loc[c_time,'minority']
    c_minority_ma=data.loc[c_time,'minority_ma']
    c_total_people=data.loc[c_time,'total_people']
    c_total_people_ma=data.loc[c_time,'total_people_ma']
    # 取下一期資料做為進場資料
    n_time=data.index[i+1]
    n_open=data.loc[n_time,'open']
    
    # 進場程序
    if position == 0 :
        if c_close > c_ma and c_minority < c_minority_ma :
            position = 1  
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
    # 出場程序
    elif position ==1 :
        # 出場邏輯
        if c_minority > c_minority_ma:
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
addp.append(mpf.make_addplot(data['ma'],color='r'))
addp.append(mpf.make_addplot(data['minority'],panel=1,secondary_y=False,color='r'))
addp.append(mpf.make_addplot(data['minority_ma'],panel=1,secondary_y=False,color='b'))

# 績效分析
Performance(trade,'ETF')
# 繪製K線圖與交易明細
ChartTrade(data,trade,addp=addp,v_enable=False)


