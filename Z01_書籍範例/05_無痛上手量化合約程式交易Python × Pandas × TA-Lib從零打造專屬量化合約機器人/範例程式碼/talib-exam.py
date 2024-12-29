#
# Author: Jackie Chang
# E-mail: ching040@gmail.com
# LineID: jackiechang040
#

from binance.um_futures import UMFutures
import logging
from binance.error import ClientError
import pandas_test as pd
import time
from datetime import datetime
import talib

API_KEY = '申請的API KEY'
SECRET_KEY = '申請的SECRET KEY'
BASE_URL = 'https://fapi.binance.com'
column = [
    'Timestamp',
    'Open',
    'High',
    'Low',
    'Close',
    'Volume',
    'Close_time',
    'Quote_av',
    'Trades',
    'Tb_base_av',
    'Tb_quote_av',
    'Ignore'
]
binsizes = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "2h":7200, "4h": 14400, "6h": 21600, "8h": 28800, "1d": 86400}

def get_kline(symbol, interval, start_time, end_time):
    try:
        res = UMFutures().klines(symbol, interval, starttime=start_time, endtime=end_time)
        return res
    except ClientError as Error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                Error.status_code, Error.error_code, Error.error_message
            )
        )
        return 0

def get_history_klines(finish_time, start_time, sizes):
    end_time = start_time + (binsizes.get(sizes) * 500 * 1000)
    a = pd.DataFrame(get_kline('ETHUSDT', sizes, start_time, end_time), columns=column)
    start_time = end_time
    while start_time < finish_time:
        end_time = start_time + (binsizes.get(sizes)*500*1000)
        b = pd.DataFrame(get_kline('ETHUSDT', sizes, start_time, end_time), columns=column)
        a = pd.concat([a, b], ignore_index=True)
        start_time = end_time
    a = a.drop_duplicates(keep='first', inplace=False, ignore_index=True)
    return a

def cal_timestamp(stamp):
    datetime_obj = datetime.strptime(stamp, '%Y-%m-%d %H:%M:%S.%f')
    start_time = int(time.mktime(datetime_obj.timetuple())*1000.0 + datetime_obj.microsecond / 1000.0)
    return start_time

if __name__=='__main__':
    finish_time = cal_timestamp(str(datetime.now()))
    start_time = cal_timestamp('2019-01-01 0:0:0.0')
    klines = get_history_klines(finish_time, start_time, '1d')
    talib_function_group = talib.get_function_groups()
    print(talib_function_group)
    print(talib_function_group.keys())














