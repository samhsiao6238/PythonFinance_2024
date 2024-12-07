#
# Author: Jackie Chang
# E-mail: ching040@gmail.com
# LineID: jackiechang040
#
from binance.um_futures import UMFutures
import logging
from binance.error import ClientError
from binance.lib.utils import config_logging
import pandas_test as pd
import time
from datetime import datetime
import talib

# 設定交易兌
SYMBOL = 'ETHUSDT'

# config_logging(logging, logging.DEBUG)
kline_data = pd.DataFrame()

# 幣安API和API網址
API_KEY = '48682b99424314bb445d38345638544e1e3bf2f6b614be1747a0e894953f0404'
SECRET_KEY = '76c9945c8dc1fb7506145a5003e5f2a0f5c6a91743fb14d11654f2e6615cd712'
BASE_URL = 'https://testnet.binancefuture.com'
# BASE_URL = 'https://fapi.binance.com'

# 繼承UMFutures類別
um_futures_client = UMFutures(key=API_KEY, secret=SECRET_KEY, base_url=BASE_URL)

# 取得USDT錢包值
def get_balance(symbol):
    try:
        wallet = 0
        response = um_futures_client.balance(recvWindow=6000)
        logging.info(response)
        for i in range(1, len(response)):
            if response[i].get('asset') == symbol:
                wallet = response[i].get('balance')
                break
        return wallet
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".
                format(error.status_code,
                       error.error_code,
                       error.error_message
            )
        )

# 取得K線數據
def get_kline(symbol, interval, limit):
    try:
        res = um_futures_client.klines(symbol, interval, limit=limit)
        return res
    except ClientError as Error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                Error.status_code, Error.error_code, Error.error_message
            )
        )
        return 0

# 取得即時價格
def get_price(symbol):
    try:
        res = float(um_futures_client.ticker_price(symbol)['price'])
        return res
    except ClientError as Error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                Error.status_code, Error.error_code, Error.error_message
            )
        )
        return 0

# 下單/平單函式
def new_order(symbol, side, quantity):
    try:
        response = um_futures_client.new_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        logging.info(response)
        return response['orderId']
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )
# 取得訂單內容及返回成交價格
def get_order(symbol, orderId):
    try:
        response = um_futures_client.get_all_orders(
            symbol=symbol,
            orderId=orderId,
            recvWindow=2000)
        logging.info(response)
        return float(response[0]['avgPrice'])
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}"
                .format(
                    error.status_code, error.error_code, error.error_message
            )
        )

# 將單筆數據讀取出來
def read_data(data, i):
    k = float(data.loc[i, 'k'])
    d = float(data.loc[i, 'd'])
    j = float(data.loc[i, 'j'])
    now_atr = float(data.loc[i, 'atr'])
    pre_atr = float(data.loc[i - 1, 'atr'])
    new_price = float(data.loc[i, 'price'])
    pre_price = float(data.loc[i - 1, 'price'])
    return k, d, j, now_atr, pre_atr, new_price, pre_price

# 指標計算
def indicator_cal():
    # 從幣安取得N根K棒
    ohlcv = pd.DataFrame(get_kline(SYMBOL, '1m', 50),
                         columns=[
                             'timestamp',
                             'open',
                             'high',
                             'low',
                             'close',
                             'volume',
                             'close_time',
                             'quote_av',
                             'trades',
                             'tb_base_av',
                             'tb_quote_av',
                             'ignore'])

    # 計算出K, D, J值
    kline_data['date_time'] = ohlcv['timestamp']
    kline_data['k'], kline_data['d'] = talib.STOCH(
                                            ohlcv['high'],
                                            ohlcv['low'],
                                            ohlcv['close'],
                                            fastk_period=9,
                                            slowk_period=3,
                                            slowd_period=3)
    kline_data['j'] = 3 * kline_data['k'] - 2 * kline_data['d']
    kline_data['price'] = ohlcv['close']

    # 計算ATR的值
    kline_data['atr'] = talib.ATR(
        ohlcv['high'],
        ohlcv['low'],
        ohlcv['close'],
        timeperiod=14)

    k, d, j, now_atr, pre_atr, new_price, pre_price = \
        read_data(kline_data, 48)

    buy_sell = ''

    if (new_price - pre_price) / pre_price > (now_atr - pre_atr) / \
            pre_atr and (now_atr > pre_atr):
        if (j < k) and (k < d) and (j < 40):
            buy_sell = 'BUY'
    elif (pre_price - new_price) / new_price > (pre_atr - now_atr) / \
            now_atr and (now_atr < pre_atr):
        if (j > k) and (k > d) and (j > 60):
            buy_sell = 'SELL'

    return buy_sell, kline_data

# 報告輸出函式
def report_csv():
    return 0

if __name__=='__main__':
    # 1. 宣告變數 -- 開單訊息
    # 交易旗標，場上是否存在交易
    trade_flag = False
    # 開單時間
    open_time = ''
    # 開單方向
    direction = ''
    # 開單價格
    open_price = 0.0
    # 2. 宣告變數 -- 資金/倉位
    # 初始資金
    start_fin = float(get_balance('USDT'))
    # 倉位管理以100為單位，每100下0.01張
    trade_num = int(start_fin / 100) * 0.01
    # 2. 宣告變數 -- 手續費
    open_fee = 0.0
    close_fee = 0.0
    # 補單次數
    dup_time = 0
    # 獲利延伸
    dup_profit = 1
    # 無限迴圈
    while True:
        new_time = time.time()
        if int(new_time) % 60 == 0:
            old_time = new_time - 60
            print(old_time, new_time)
            break
    while True:
        if not trade_flag:
            new_time = time.time()
            # print(new_time, old_time)
            if new_time - old_time >= 60:
                # 判斷當前方向
                print('start_time = {}'.format(datetime.now()))
                direction, kline_data = indicator_cal()
                print('end_time = {}'.format(datetime.now()))
                print(datetime.now())
                # print(kline_data)
                if direction != '':
                    open_time = datetime.now()
                    orderId = new_order(SYMBOL, direction, trade_num)
                    open_price = get_order(SYMBOL, orderId)
                    trade_flag = True
                    open_fee = open_price / 20 * trade_num * 0.0004
                    print('開單日期: {} 開單價格: {} 開單數量: {} 開單手續費: {}'
                          .format(open_time, open_price, trade_num, open_fee))
                old_time = new_time
        elif trade_flag:
            new_time = time.time()
            if new_time - old_time >= 60:
                # 方向為BUY時
                now_price = get_price(SYMBOL)
                new_time = time.time()
                if new_time - old_time >= 60:
                    now_direction, kline_data = indicator_cal()
                    old_time = new_time
                else:
                    now_direction = direction
                if direction == 'BUY':
                    if now_price - open_price > 120 * dup_profit:
                        if now_direction == '' or now_direction == 'SELL':
                            orderId = new_order(SYMBOL, 'SELL', trade_num)
                            close_price = get_order(SYMBOL, orderId)
                            close_fee = close_price / 20 * trade_num * 0.0002
                            profit = (close_price - open_price) * trade_num \
                                     - open_fee - close_fee
                            open_fee2 = ''
                            dup_time = 0
                            direction = ''
                            open_time = ''
                            open_price = 0.0
                            dup_profit = 1
                            start_fin = float(get_balance('USDT'))
                            trade_num = int(start_fin/100) * 0.01
                            trade_flag = False
                        else:
                            dup_profit += 1
                    elif now_price - open_price < -100 * (dup_time+1):
                        if dup_time < 2:
                            orderId = new_order(SYMBOL, direction, trade_num*2)
                            temp_price = get_order(SYMBOL, orderId)
                            open_price = (open_price + temp_price * 2) / 3
                            open_fee = open_fee + \
                                       (temp_price / 20 * trade_num * 2 * 0.0002)
                            trade_num = trade_num + (trade_num * 2)
                            dup_time = dup_time + 1

                    if dup_time >= 2:
                        if now_price - open_price > 50 * dup_profit:
                            if now_direction == '' or now_direction == 'SELL':
                                orderId = new_order(SYMBOL, 'SELL', trade_num)
                                close_price = get_order(SYMBOL, orderId)
                                close_fee = close_price / 20 * trade_num * 0.0002
                                profit = (close_price - open_price) * trade_num \
                                         - open_fee - close_fee
                                open_fee2 = ''
                                dup_time = 0
                                direction = ''
                                open_time = ''
                                open_price = 0.0
                                dup_profit = 1
                                start_fin = float(get_balance('USDT'))
                                trade_num = int(start_fin / 100) * 0.01
                                trade_flag = False
                            else:
                                dup_profit += 1

                elif direction == 'SELL':
                    if open_price - now_price > 120 * dup_profit:
                        if now_direction == '' or now_direction == 'BUY':
                            orderId = new_order(SYMBOL, 'BUY', trade_num)
                            close_price = get_order(SYMBOL, orderId)
                            close_fee = close_price / 20 * trade_num * 0.0002
                            profit = (open_price - close_price) * trade_num \
                                     - open_fee - close_fee
                            dup_time = 0
                            direction = ''
                            open_time = ''
                            open_price = 0.0
                            dup_profit = 1
                            start_fin = float(get_balance('USDT'))
                            trade_num = int(start_fin / 100) * 0.01
                            trade_flag = False
                    elif open_price - now_price < -100 * (dup_time + 1):
                        if dup_time < 2:
                            orderId = new_order(SYMBOL, direction, trade_num*2)
                            temp_price = get_order(SYMBOL, orderId)
                            open_price = (open_price + temp_price * 2) / 3
                            open_fee = open_fee + \
                                       (temp_price / 20 * trade_num * 2 * 0.0002)
                            trade_num = trade_num + (trade_num * 2)
                            dup_time = dup_time + 1
                    if dup_time >= 2:
                        if open_price - now_price > 50 * dup_profit:
                            if now_direction == '' or now_direction == 'BUY':
                                orderId = new_order(SYMBOL, 'BUY', trade_num)
                                close_price = get_order(SYMBOL, orderId)
                                close_fee = (close_price / 20 * trade_num * 0.0002)
                                profit = ((open_price - close_price) * trade_num) \
                                         - open_fee - close_fee
                                dup_time = 0
                                direction = ''
                                open_time = ''
                                open_price = 0.0
                                start_fin = float(get_balance('USDT'))
                                trade_num = int(start_fin / 100) * 0.01
                                trade_flag = False
                            else:
                                dup_profit += 1


