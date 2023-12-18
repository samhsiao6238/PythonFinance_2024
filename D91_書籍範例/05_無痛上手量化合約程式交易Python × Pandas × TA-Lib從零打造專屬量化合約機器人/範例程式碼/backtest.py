#
# Author: Jackie Chang
# E-mail: ching040@gmail.com
# LineID: jackiechang040
#
from binance.um_futures import UMFutures
import logging
from binance.error import ClientError
# from binance.lib.utils import config_logging
import pandas as pd
import time
from datetime import datetime
import talib
import csv
import os

column = [
    'open_time',
    'open',
    'high',
    'low',
    'close',
    'VOL',
    'close_time',
    'trade_vol',
    'trade_num',
    'Buy_Trade',
    'sell_trade',
    'nothing']

FinBase = 10000
INTERVAL = '1m'
START_KLINE = '2022-01-01 0:0:0.0'

binsizes = {
    "1m": 60,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "8h": 28800,
    "1d": 86400}

def get_kline(symbol, interval, start_time, end_time, limit):
    try:
        res = UMFutures().klines(
            symbol,
            interval,
            starttime=start_time,
            endtime=end_time,
            limit=limit)
        return res
    except ClientError as Error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}"
            .format(
                Error.status_code, Error.error_code, Error.error_message
            )
        )
        return 0

def get_history_klines(sizes, limit):
    finish_time = cal_timestamp(str(datetime.now()))
    start_time = cal_timestamp(START_KLINE)
    end_time = start_time + (binsizes.get(sizes) * limit * 1000)
    a = pd.DataFrame(get_kline(
                        'ETHUSDT',
                        sizes,
                        start_time,
                        end_time,
                        limit),
                    columns=column)
    start_time = end_time
    while start_time < finish_time:
        end_time = start_time + (binsizes.get(sizes)*limit*1000)
        b = pd.DataFrame(get_kline(
                            'ETHUSDT',
                            sizes,
                            start_time,
                            end_time,
                            limit),
                        columns=column)
        a = pd.concat([a, b], ignore_index=True)
        start_time = end_time
    a.drop_duplicates(
        keep='first',
        inplace=False,
        ignore_index=True)
    a['open_time'] = pd.to_datetime(a['open_time'], unit='ms')
    a['close_time'] = pd.to_datetime(a['close_time'], unit='ms')
    return a

def cal_timestamp(stamp):
    datetime_obj = datetime.strptime(
                    stamp,
                    '%Y-%m-%d %H:%M:%S.%f')
    start_time = int(time.mktime(
                        datetime_obj.timetuple())*1000.0 +
                        datetime_obj.microsecond / 1000.0)
    return start_time

# 將單筆數據讀取出來
def read_data(kline_data, i):
    k = float(kline_data.loc[i, 'k'])
    d = float(kline_data.loc[i, 'd'])
    j = float(kline_data.loc[i, 'j'])
    now_atr = float(kline_data.loc[i, 'atr'])
    pre_atr = float(kline_data.loc[i - 1, 'atr'])
    new_price = float(kline_data.loc[i, 'price'])
    pre_price = float(kline_data.loc[i - 1, 'price'])
    return k, d, j, now_atr, pre_atr, new_price, pre_price

# 提前計算buy或Sell的訊號
def PreInit():
    # 讀取K棒數據
    ohlcv = get_history_klines(INTERVAL, 1500)
    # 宣告一個空的DataFrame
    kline_data = pd.DataFrame()
    # 將當前時間存入data中
    kline_data['date_time'] = ohlcv['open_time']
    # 計算KDJ/BOLL值, 並存入data中
    kline_data['k'], kline_data['d'] = talib.STOCH(
        ohlcv['high'],
        ohlcv['low'],
        ohlcv['close'],
        fastk_period=9,
        slowk_period=3,
        slowd_period=3)
    kline_data['j'] = 3 * kline_data['k'] - 2 * kline_data['d']
    # 設定buy_sell欄位為空值
    kline_data['buy_sell'] = ''
    # 寫入收盤價
    kline_data['price'] = ohlcv['close']
    kline_data['atr'] = talib.ATR(
        ohlcv['high'],
        ohlcv['low'],
        ohlcv['close'], timeperiod=14)

    for i in range(1, len(kline_data)):
        k, d, j, now_atr, pre_atr, new_price, pre_price = \
            read_data(kline_data, i)
        if (new_price - pre_price) / pre_price > (now_atr - pre_atr) \
                / pre_atr and (now_atr > pre_atr):
            if (j < k) and (k < d) and (j < 40):
                kline_data.loc[i, 'buy_sell'] = 'BUY'
        elif (pre_price - new_price) / new_price > (pre_atr - now_atr) \
                / now_atr and (now_atr < pre_atr):
            if (j > k) and (k > d) and (j > 60):
                kline_data.loc[i, 'buy_sell'] = 'SELL'

    # 返回數據
    return kline_data


# 寫report.csv檔
def report_csv(i, trade_flag, open_time, direction, open_price, close_time,
               close_price, trade_num, profit, open_fee, close_fee):
    report_data = [i, trade_flag, open_time, direction, open_price, close_time,
                   close_price, trade_num, profit, open_fee, close_fee]
    filename = r'.\report.csv'
    f = open(filename, 'a', newline='')
    csv_writer = csv.writer(f, dialect='excel')
    csv_writer.writerow(report_data)


# 回測函式
def back_test(kline_data):
    # 交易旗標
    trade_flag = False
    # 開單時間
    open_time = ''
    # 開單方向
    direction = ''
    # 開單價格
    open_price = 0.0
    # 初始資金
    start_fin = FinBase
    # 每次下單張數100為單位, 每100下0.01張
    trade_num = int(start_fin/100) * 0.01
    # 補單次數
    dup_time = 0
    # 獲利延伸
    dup_profit = 1
    open_fee = 0.0
    close_fee = 0.0
    # 判斷report.csv和data.csv是否存在, 存在便刪除
    if os.path.isfile('report.csv'):
        os.remove('report.csv')
    if os.path.isfile('data.csv'):
        os.remove('data.csv')
    # 將整理好的數據寫入data.csv可用做比對數據用
    kline_data.to_csv('data.csv')
    # 逐筆取出buy_sell訊號, 並進行買入及平單模擬記錄
    for i in range(0, len(kline_data)):
        # 未開單的情況
        if not trade_flag:
            # 當direction為none, 且buy_sell不為0時, 依buy_sell進行買入設置
            if direction == '':
                if kline_data.loc[i, 'buy_sell'] != '':
                    open_time = kline_data.loc[i, 'date_time']
                    open_price = float(kline_data.loc[i, 'price'])
                    direction = kline_data.loc[i, 'buy_sell']
                    trade_flag = True
                    open_fee = float(kline_data.loc[i, 'price'])/20*trade_num*0.0004
                    report_csv(i, trade_flag, open_time, direction, open_price, '',
                               '',
                               trade_num, '', open_fee, '')
        # 開單時
        if trade_flag:
            # 方向為BUY時
            if direction == 'BUY':
                if float(kline_data.loc[i, 'price']) - open_price > 120*dup_profit:
                    if (kline_data.loc[i, 'buy_sell'] == '') or \
                            (kline_data.loc[i, 'buy_sell'] == 'SELL'):
                        close_fee = (float(kline_data.loc[i, 'price'])/20*trade_num/100)
                        profit = ((float(kline_data.loc[i, 'price']) - open_price) * trade_num) - open_fee - close_fee
                        report_csv(i, trade_flag, open_time, direction, open_price, kline_data.loc[i, 'date_time'], kline_data.loc[i, 'price'], trade_num, profit, open_fee, '')
                        dup_time = 0
                        direction = ''
                        open_time = ''
                        open_price = 0.0
                        dup_profit = 1
                        start_fin = start_fin + profit
                        trade_num = int(start_fin/100) * 0.01
                        trade_flag = False
                    else:
                        dup_profit += 1
                elif float(kline_data.loc[i, 'price']) - open_price < -100 * (dup_time+1):
                    if dup_time < 2:
                        open_price = (open_price + float(kline_data.loc[i, 'price']) * 2) / 3
                        open_fee = open_fee + (float(kline_data.loc[i, 'price']) / 20 * trade_num * 2 / 100)
                        report_csv(i, trade_flag, kline_data.loc[i, 'date_time'], direction, open_price, '',
                                   '',
                                   trade_num * 2, '', open_fee, '')
                        trade_num = trade_num + (trade_num * 2)
                        dup_time = dup_time + 1
                if dup_time >= 2:
                    if float(kline_data.loc[i, 'price']) - open_price > 50 * dup_profit:
                        if kline_data.loc[i, 'buy_sell'] == '' or kline_data.loc[i, 'buy_sell'] == 'SELL':
                            close_fee = (float(kline_data.loc[i, 'price']) / 20 * trade_num / 100)
                            profit = (float(kline_data.loc[i, 'price']) - open_price) * trade_num - open_fee - close_fee
                            report_csv(i, trade_flag, open_time, direction, open_price, kline_data.loc[i, 'date_time'], kline_data.loc[i, 'price'],
                                           trade_num, profit, '', close_fee)
                            dup_time = 0
                            direction = ''
                            open_time = ''
                            open_price = 0.0
                            dup_profit = 1
                            start_fin = start_fin + profit
                            trade_num = int(start_fin / 100) * 0.01
                            trade_flag = False
                        else:
                            dup_profit += 1
            elif direction == 'SELL':
                if open_price - float(kline_data.loc[i, 'price']) > 120 * dup_profit:
                    if kline_data.loc[i, 'buy_sell'] == '' or kline_data.loc[i, 'buy_sell'] == 'BUY':
                        close_fee = (float(kline_data.loc[i, 'price']) / 20 * trade_num / 100)
                        profit = (open_price - float(kline_data.loc[i, 'price'])) * trade_num - open_fee - close_fee
                        report_csv(i, trade_flag, open_time, direction, open_price, kline_data.loc[i, 'date_time'], kline_data.loc[i, 'price'], trade_num, profit, '', close_fee)
                        dup_time = 0
                        direction = ''
                        open_time = ''
                        open_price = 0.0
                        dup_profit = 1
                        start_fin = start_fin + profit
                        trade_num = int(start_fin / 100) * 0.01
                        trade_flag = False
                elif open_price - float(kline_data.loc[i, 'price']) < -100 * (dup_time+1):
                    if dup_time < 2:
                        open_price = (open_price + float(kline_data.loc[i, 'price']) * 2) / 3
                        open_fee = open_fee + (float(kline_data.loc[i, 'price']) / 20 * trade_num * 2 / 100)
                        report_csv(i, trade_flag, kline_data.loc[i, 'date_time'], direction, open_price, '',
                                   '',
                                   trade_num * 2, '', open_fee, '')
                        trade_num = trade_num + (trade_num * 2)
                        dup_time = dup_time + 1
                if dup_time >= 2:
                    if open_price - float(kline_data.loc[i, 'price']) > 50 * dup_profit:
                        if kline_data.loc[i, 'buy_sell'] == '' or kline_data.loc[i, 'buy_sell'] == 'BUY':
                            close_fee = (float(kline_data.loc[i, 'price']) / 20 * trade_num / 100)
                            profit = ((open_price - float(kline_data.loc[i, 'price'])) * trade_num) - open_fee - close_fee
                            report_csv(i, trade_flag, open_time, direction, open_price, kline_data.loc[i, 'date_time'], kline_data.loc[i, 'price'],
                                           trade_num, profit, '', close_fee)
                            dup_time = 0
                            direction = ''
                            open_time = ''
                            open_price = 0.0
                            start_fin = start_fin + profit
                            trade_num = int(start_fin / 100) * 0.01
                            trade_flag = False
                        else:
                            dup_profit += 1
    print('錢包總額:', start_fin)
    print('總盈利:', start_fin - FinBase)


if __name__ == '__main__':
    start_time = datetime.now()
    print(start_time)
    # print(datetime.now())
    data = PreInit()
    back_test(data)
    end_time = datetime.now()
    print('總筆數:', len(data))
    print('回測總耗時:', end_time - start_time)
    print(start_time, datetime.now())
