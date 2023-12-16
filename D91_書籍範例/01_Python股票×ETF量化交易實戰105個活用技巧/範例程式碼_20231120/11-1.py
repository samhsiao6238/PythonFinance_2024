# 載入必要套件
from Data import getDataFM,getStockList
from BackTest import ChartTrade,Performance
import pandas as pd
import mplfinance as mpf
from talib.abstract import SMA

# 取得股票代碼
stock_list=getStockList()
stocks=stock_list[(stock_list['產業別']=='半導體業')&(stock_list['市場別']=='上市')]['有價證券代號及名稱'].str.split('　').str[0]

# 將每個同產業的股票依序回測
for prod in stocks:
    print(prod)
    # 取得回測資料
    try:
        data=getDataFM(prod,'2010-01-01','2022-05-01')
    except:
        continue 
            
    # 計算簡單移動平均線
    data['ma1']=data['close'].rolling(60).mean()
    data['ma2']=data['close'].rolling(120).mean()

    # 初始部位
    position=0
    trade=pd.DataFrame()
    # 開始回測
    for i in range(data.shape[0]-1):
        # 取得策略會應用到的變數
        c_time=data.index[i]
        c_high=data.loc[c_time,'high']
        c_close=data.loc[c_time,'close']
        c_ma1=data.loc[c_time,'ma1']
        c_ma2=data.loc[c_time,'ma2']
        # 取下一期資料做為進場資料
        n_time=data.index[i+1]
        n_open=data.loc[n_time,'open']
        
        # 進場程序
        if position ==0  :
            # 進場邏輯
            if c_ma1 > c_ma2  :
                position = 1  
                order_i=i
                order_time=n_time
                order_price=n_open
                order_unit=1
        # 出場程序
        elif position ==1 :
            # 出場邏輯
            if c_ma1 < c_ma2 :
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
    
    print('回測商品代碼:',prod)
    Performance(trade,'Stock')
    print('----------------------------------')


