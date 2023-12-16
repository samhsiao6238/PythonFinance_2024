# 載入必要套件
from Data import getFMPriceAndMarginTrade
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf

# 取得回測資料
prod='2330'
data=getFMPriceAndMarginTrade(prod,'2019-01-01','2022-05-01')

# 融資融券餘額
data['mb']=data['MarginPurchaseTodayBalance'].astype(int)
data['ms']=data['ShortSaleTodayBalance'].astype(int)
data['mb_mean']=data['mb'].rolling(20).mean()
data['ms_mean']=data['ms'].rolling(20).mean()

# 初始部位
position=0
trade=pd.DataFrame()
# 開始回測
for i in range(data.shape[0]-1):
    # 取得策略會應用到的變數
    c_time=data.index[i]
    c_high=data.loc[c_time,'high']
    c_close=data.loc[c_time,'close']
    c_mb=data.loc[c_time,'mb']
    c_mb_mean=data.loc[c_time,'mb_mean']
    c_ms=data.loc[c_time,'ms']
    c_ms_mean=data.loc[c_time,'ms_mean']
    # 取下一期資料做為進場資料
    n_time=data.index[i+1]
    n_open=data.loc[n_time,'open']
    
    # 進場程序
    if position == 0 :
        if c_mb < c_mb_mean*0.99 and c_ms > c_ms_mean*1.01 :
            position = 1  
            order_i=i
            order_time=n_time
            order_price=n_open
            order_unit=1
    # 出場程序
    elif position ==1 :
        # 出場邏輯
        if c_ms < c_ms_mean  :
            position = 0
            cover_time=n_time
            cover_price=n_open
            # 交易紀錄
            trade=trade._append(pd.Series([
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
addp.append(mpf.make_addplot(data['mb'],panel=1,color='red',secondary_y=False))
# addp.append(mpf.make_addplot(data['mb_mean'],panel=1,color='blue',secondary_y=False))
addp.append(mpf.make_addplot(data['ms'],panel=2,color='red',secondary_y=False))
# addp.append(mpf.make_addplot(data['ms_mean'],panel=2,color='blue',secondary_y=False))

# 績效分析
Performance(trade,'Stock')
# 繪製K線圖與交易明細
ChartTrade(data,trade,addp=addp,v_enable=False)



