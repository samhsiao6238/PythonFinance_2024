from FinMind.data import DataLoader
import pandas as pd
import yfinance as yf
import sys
import numpy as np
import os
import time
import requests
import warnings

warnings.filterwarnings("ignore")

# 載入yahoo finance 套件

# 載入FinMind 套件

FM = DataLoader()

datapath = "data"

# 取得yahoo finance 資料


def getDataYF(prod, st, en):
    # 取得資料
    tmpdata = yf.download(prod, start=st, end=en)
    # 將所有的欄位改為小寫
    tmpdata.columns = [i.lower() for i in tmpdata.columns]
    # 回傳資料
    return tmpdata

# 更新資料源為 yahoo finance


def getDataFM(prod, st, en):
    bakfile = 'data//YF_%s_%s_%s_stock_daily_adj.csv' % (prod, st, en)
    if os.path.exists(bakfile):
        data = pd.read_csv(bakfile)
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date')
    else:
        data = yf.download(f"{prod}.TW", start=st, end=en)
        data.columns = [i.lower() for i in data.columns]
        # 除錯 如果沒有資料
        if data.shape[0] == 0:
            print('沒有資料')
            return pd.DataFrame()
        # 將資料寫入備份檔
        data.to_csv(bakfile)
    return data


# 取得載入FinMind 還原股價資料
"""
def getDataFM(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_stock_daily_adj.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        # 取得必要欄位
        tmpdata = tmpdata[["open", "high", "low", "close", "volume"]]
    # 沒有的話就取API內容
    else:
        tmpdata = FM.taiwan_stock_daily_adj(stock_id=prod, start_date=st, end_date=en)
        # 取得資料
        tmpdata = tmpdata.rename(
            columns={"max": "high", "min": "low", "Trading_Volume": "volume"}
        )
        # 取得資料錯誤
        if tmpdata.shape[0] == 0:
            print(prod, st, en, "無法取得資料")
            sys.exit()
        # 將日期設定為索引
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        # 取得必要欄位
        tmpdata = tmpdata[["open", "high", "low", "close", "volume"]]
        # 將API內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata
"""

# 取得載入FinMind 股權分散表資料


def getFMShareHolder(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_stock_holding_shares_per.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
    # 沒有的話就取API內容
    else:
        tmpdata = FM.taiwan_stock_holding_shares_per(
            stock_id=prod, start_date=st, end_date=en
        )
        # 將日期設定為索引
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        tmpdata.drop("date", axis=1, inplace=True)
        # 將API內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata


# 將股權分散表轉換為一日一筆
def ShareHolderWeekly(data):
    rs_sh, rs_dt = [], []
    # 依照日期去將資料做整合
    for dt in data.index.unique():
        # 撈出當天的所有資料
        data1 = data[data.index == dt]
        # 依照不同級距 轉換為特定欄位
        tmprow = data1.loc[data1["HoldingSharesLevel"]
                           == "1-999", "percent"].values
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"]
                      == "1,000-5,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"] ==
                      "5,001-10,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"] ==
                      "10,001-15,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"] ==
                      "15,001-20,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"] ==
                      "20,001-30,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"] ==
                      "30,001-40,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[data1["HoldingSharesLevel"] ==
                      "40,001-50,000", "percent"].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "50,001-100,000", "percent"
            ].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "100,001-200,000", "percent"
            ].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "200,001-400,000", "percent"
            ].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "400,001-600,000", "percent"
            ].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "600,001-800,000", "percent"
            ].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "800,001-1,000,000", "percent"
            ].values,
        )
        tmprow = np.append(
            tmprow,
            data1.loc[
                data1["HoldingSharesLevel"] == "more than 1,000,001", "percent"
            ].values,
        )
        # 總股東人數
        tmprow = np.append(
            tmprow, data1.loc[data1["HoldingSharesLevel"]
                              == "total", "people"].values
        )
        # 將DF資料存放到容器
        rs_sh.append(tmprow)
        # 資料日期存成一個列表
        rs_dt.append(dt)
    # 將每日的資料整合
    rs = pd.DataFrame(
        rs_sh,
        index=rs_dt,
        columns=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "total_people",
        ],
    )
    return rs


# 取得價格與股權分散表
def getPriceAndShareHolder(prod, st, en):
    data1 = getDataFM(prod, st, en)
    data2 = getFMShareHolder(prod, st, en)
    data2a = ShareHolderWeekly(data2)
    # 從每個股權分散的資料 去抓出開高低收
    for i in range(1, data2a.shape[0]):
        tmpdata = data1.loc[
            (data1.index > data2a.index[i - 1]
             ) & (data1.index <= data2a.index[i]),
        ]
        # 如果沒有資料 可能遇到連假
        if tmpdata.shape[0] == 0:
            # 移除資料
            continue
        data2a.loc[data2a.index[i],
                   "open"] = tmpdata.loc[tmpdata.index[0], "open"]
        data2a.loc[data2a.index[i], "high"] = tmpdata.loc[:, "high"].max()
        data2a.loc[data2a.index[i], "low"] = tmpdata.loc[:, "low"].min()
        data2a.loc[data2a.index[i],
                   "close"] = tmpdata.loc[tmpdata.index[-1], "close"]
        data2a.loc[data2a.index[i], "volume"] = tmpdata.loc[:, "volume"].sum()
    data2a = data2a.dropna()
    return data2a


# 取得三大法人 證交所資料來源
def getTSEInstitutionalInvestors(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_TSE_InstitutionalInvestorsBuySell.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"])
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
        # 將資料內容轉換為數值
        # for i in range(2,tmpdata.shape[1]):
        # tmpdata.iloc[:,i].astype(int)
    # 沒有的話就取檔案內容
    else:
        # 取得檔案內容
        tmpdata = pd.read_csv("三大法人爬蟲資料.csv", encoding="cp950")
        tmpdata = tmpdata[
            (tmpdata["證券代號"] == prod)
            & (tmpdata["日期"] >= int(st))
            & (tmpdata["日期"] <= int(en))
        ]
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"], format="%Y%m%d")
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
        # 將資料內容轉換為數值
        for i in range(2, tmpdata.shape[1]):
            tmpdata.iloc[:, i] = tmpdata.iloc[:, i].str.replace(",", "")
            tmpdata.iloc[:, i].astype(int)
        # 將單一證券內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata


# 取得三大法人 FinMind資料來源
def getFMInstitutionalInvestors(prod, st, en):
    # 備份檔名
    bakfile = (
        f"{datapath}\\{prod}_{st}_{en}_TaiwanStockInstitutionalInvestorsBuySell.csv"
    )
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
    # 沒有的話就取API內容
    else:
        tmpdata = FM.taiwan_stock_institutional_investors(
            stock_id=prod, start_date=st, end_date=en
        )
        # 將日期設定為索引
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        tmpdata.drop("date", axis=1, inplace=True)
        # 將API內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata


# 將三大法人轉換為一日一筆
def InstInvestorsDaily(data):
    rs_sh, rs_dt = [], []
    # 依照日期去將資料做整合
    for dt in data.index.unique():
        # 撈出當天的所有資料
        data1 = data[data.index == dt]
        # 依照不同交易人類別
        tmprow = []
        f_b = data1.loc[data1["name"] == "Foreign_Investor", "buy"].values
        f_s = data1.loc[data1["name"] == "Foreign_Investor", "sell"].values
        fd_b = data1.loc[data1["name"] == "Foreign_Dealer_Self", "buy"].values
        fd_s = data1.loc[data1["name"] == "Foreign_Dealer_Self", "sell"].values
        i_b = data1.loc[data1["name"] == "Investment_Trust", "buy"].values
        i_s = data1.loc[data1["name"] == "Investment_Trust", "sell"].values
        d_b = data1.loc[data1["name"] == "Dealer", "buy"].values
        d_s = data1.loc[data1["name"] == "Dealer", "sell"].values
        ds_b = data1.loc[data1["name"] == "Dealer_self", "buy"].values
        ds_s = data1.loc[data1["name"] == "Dealer_self", "sell"].values
        dh_b = data1.loc[data1["name"] == "Dealer_Hedging", "buy"].values
        dh_s = data1.loc[data1["name"] == "Dealer_Hedging", "sell"].values
        # 如果為空 則填入該欄位為0
        if len(f_b) == 0:
            tmprow.append(0)
        else:
            tmprow.append(f_b[0])
        if len(f_s) == 0:
            tmprow.append(0)
        else:
            tmprow.append(f_s[0])
        if len(fd_b) == 0:
            tmprow.append(0)
        else:
            tmprow.append(fd_b[0])
        if len(fd_s) == 0:
            tmprow.append(0)
        else:
            tmprow.append(fd_s[0])
        if len(i_b) == 0:
            tmprow.append(0)
        else:
            tmprow.append(i_b[0])
        if len(i_s) == 0:
            tmprow.append(0)
        else:
            tmprow.append(i_s[0])
        if len(d_b) == 0:
            tmprow.append(0)
        else:
            tmprow.append(d_b[0])
        if len(d_s) == 0:
            tmprow.append(0)
        else:
            tmprow.append(d_s[0])
        if len(ds_b) == 0:
            tmprow.append(0)
        else:
            tmprow.append(ds_b[0])
        if len(ds_s) == 0:
            tmprow.append(0)
        else:
            tmprow.append(ds_s[0])
        if len(dh_b) == 0:
            tmprow.append(0)
        else:
            tmprow.append(dh_b[0])
        if len(dh_s) == 0:
            tmprow.append(0)
        else:
            tmprow.append(dh_s[0])
        # 將DF資料存放到容器
        rs_sh.append(tmprow)
        # 資料日期存成一個列表
        rs_dt.append(dt)
    # 將每日的資料整合
    rs = pd.DataFrame(
        rs_sh,
        index=rs_dt,
        columns=[
            "外陸資買進股數(不含外資自營商)",
            "外陸資賣出股數(不含外資自營商)",
            "外資自營商買進股數",
            "外資自營商賣出股數",
            "投信買進股數",
            "投信賣出股數",
            "自營商買進股數(自行買賣)_1",
            "自營商賣出股數(自行買賣)_1",
            "自營商買進股數(自行買賣)_2",
            "自營商賣出股數(自行買賣)_2",
            "自營商買進股數(避險)",
            "自營商賣出股數(避險)",
        ],
    )
    # 由於FinMind的，自營商類別有兩個，所以必須將這個了欄位合併，
    rs["自營商買進股數(自行買賣)"] = rs["自營商買進股數(自行買賣)_1"] + rs["自營商買進股數(自行買賣)_2"]
    rs["自營商賣出股數(自行買賣)"] = rs["自營商賣出股數(自行買賣)_1"] + rs["自營商賣出股數(自行買賣)_2"]
    rs.drop("自營商買進股數(自行買賣)_1", axis=1, inplace=True)
    rs.drop("自營商買進股數(自行買賣)_2", axis=1, inplace=True)
    rs.drop("自營商賣出股數(自行買賣)_1", axis=1, inplace=True)
    rs.drop("自營商賣出股數(自行買賣)_2", axis=1, inplace=True)
    return rs


# 取得K線與三大法人的集合資料 透過 證交所
def getPriceAndInstInvest_TSE(prod, st, en):
    # 取得還原股價
    data1 = getDataFM(prod, st, en)
    # 取得證交所的三大法人
    st = st.replace("-", "")
    en = en.replace("-", "")
    data2 = getTSEInstitutionalInvestors(prod, st, en)
    data3 = pd.concat([data1, data2], axis=1, join="inner")
    return data3


# 取得K線與三大法人的集合資料 透過 FinMind
def getPriceAndInstInvest_FM(prod, st, en):
    # 取得還原股價
    data1 = getDataFM(prod, st, en)
    # 取得三大法人
    data2 = getFMInstitutionalInvestors(prod, st, en)
    # 轉換資料格式
    data2_1 = InstInvestorsDaily(data2)
    data3 = pd.concat([data1, data2_1], axis=1, join="inner")
    return data3


# 取得融資融券 證交所資料來源
def getTSEMarginTrading(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_TSE_MarginTrading.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"])
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
    # 沒有的話就取檔案內容
    else:
        # 取得檔案內容
        tmpdata = pd.read_csv("融資融券爬蟲資料.csv", encoding="cp950")
        tmpdata = tmpdata[
            (tmpdata["股票代號"] == prod)
            & (tmpdata["日期"] >= int(st))
            & (tmpdata["日期"] <= int(en))
        ]
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"], format="%Y%m%d")
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
        # 將資料內容轉換為數值
        for i in range(2, tmpdata.shape[1] - 1):
            tmpdata.iloc[:, i] = tmpdata.iloc[:, i].str.replace(",", "")
            tmpdata.iloc[:, i].astype(int)
        # 將單一證券內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    tmpdata.columns = [
        "股票代號",
        "股票名稱",
        "融資買進",
        "融資賣出",
        "融資現金償還",
        "融資前日餘額",
        "融資今日餘額",
        "融資限額",
        "融券買進",
        "融券賣出",
        "融券現券償還",
        "融券前日餘額",
        "融券今日餘額",
        "融券限額",
        "資券互抵",
        "註記",
    ]
    return tmpdata


# 取得融資融券 FinMind資料來源
def getFMMarginTrading(prod, st, en):
    # 備份檔名
    bakfile = (
        f"{datapath}\\{prod}_{st}_{en}_taiwan_stock_margin_purchase_short_sale.csv"
    )
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
    # 沒有的話就取API內容
    else:
        tmpdata = FM.taiwan_stock_margin_purchase_short_sale(
            stock_id=prod, start_date=st, end_date=en
        )
        # 將日期設定為索引
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        tmpdata.drop("date", axis=1, inplace=True)
        # 將API內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata


# 取得融券借券 證交所資料來源
def getTSEShortSales(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_TSE_ShortSales.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"])
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
    # 沒有的話就取檔案內容
    else:
        # 取得檔案內容
        tmpdata = pd.read_csv("融券借券爬蟲資料.csv", encoding="cp950")
        tmpdata = tmpdata[
            (tmpdata["股票代號"] == prod)
            & (tmpdata["日期"] >= int(st))
            & (tmpdata["日期"] <= int(en))
        ]
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"], format="%Y%m%d")
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
        # 將資料內容轉換為數值
        for i in range(2, tmpdata.shape[1] - 1):
            tmpdata.iloc[:, i] = tmpdata.iloc[:, i].str.replace(",", "")
            tmpdata.iloc[:, i].astype(int)
        # 將單一證券內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    tmpdata.columns = [
        "股票代號",
        "股票名稱",
        "融券前日餘額",
        "融券賣出",
        "融券買進",
        "融券現券",
        "融券今日餘額",
        "融券限額",
        "借券前日餘額",
        "借券當日賣出",
        "借券當日還券",
        "借券當日調整",
        "借券當日餘額",
        "次一營業日可限額",
        "備註",
    ]
    return tmpdata


# 取得融券借券 FinMind資料來源
def getFMShortSales(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_taiwan_daily_short_sale_balances.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
    # 沒有的話就取API內容
    else:
        tmpdata = FM.taiwan_daily_short_sale_balances(
            stock_id=prod, start_date=st, end_date=en
        )
        # 將日期設定為索引
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        tmpdata.drop("date", axis=1, inplace=True)
        # 將API內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata


# 取得股價以及融資融券 證交所資料來源
def getTSEPriceAndMarginTrade(prod, st, en):
    data1 = getDataFM(prod, st, en)
    # 取得證交所的融資融券
    st = st.replace("-", "")
    en = en.replace("-", "")
    data2 = getTSEMarginTrading(prod, st, en)
    data3 = pd.concat([data1, data2], axis=1, join="inner")
    return data3


# 取得股價以及融券借券 證交所資料來源
def getTSEPriceAndShortSales(prod, st, en):
    data1 = getDataFM(prod, st, en)
    # 取得證交所的融券借券
    st = st.replace("-", "")
    en = en.replace("-", "")
    data2 = getTSEShortSales(prod, st, en)
    data3 = pd.concat([data1, data2], axis=1, join="inner")
    return data3


# 取得股價以及融資融券 FinMind資料來源
def getFMPriceAndMarginTrade(prod, st, en):
    data1 = getDataFM(prod, st, en)
    data2 = getFMMarginTrading(prod, st, en)
    data3 = pd.concat([data1, data2], axis=1, join="inner")
    return data3


# 取得股價以及融券借券 FinMind資料來源
def getFMPriceAndShortSales(prod, st, en):
    data1 = getDataFM(prod, st, en)
    data2 = getFMShortSales(prod, st, en)
    data3 = pd.concat([data1, data2], axis=1, join="inner")
    return data3


# 取得 公開資訊 月營收
def getTSEMonthRevenue(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_TSE_MonthRevenue.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"])
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
    # 沒有的話就取檔案內容
    else:
        # 取得檔案內容
        tmpdata = pd.read_csv("月營收爬蟲資料.csv", encoding="cp950")
        tmpdata = tmpdata[
            (tmpdata["公司代號"] == int(prod))
            & (tmpdata["日期"] >= int(st))
            & (tmpdata["日期"] <= int(en))
        ]
        tmpdata["日期"] = pd.to_datetime(tmpdata["日期"], format="%Y%m%d")
        tmpdata = tmpdata.set_index(tmpdata["日期"])
        tmpdata.drop("日期", axis=1, inplace=True)
        # 將單一證券內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    tmpdata = tmpdata.drop_duplicates()
    return tmpdata


# 取得 FinMind 月營收
def getFMMonthRevenue(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}\\{prod}_{st}_{en}_taiwan_stock_month_revenue.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        tmpdata = pd.read_csv(bakfile)
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
    # 沒有的話就取API內容
    else:
        tmpdata = FM.taiwan_stock_month_revenue(stock_id=prod, start_date=st)
        # 將日期設定為索引
        tmpdata["date"] = pd.to_datetime(tmpdata["date"])
        tmpdata = tmpdata.set_index(tmpdata["date"])
        tmpdata.drop("date", axis=1, inplace=True)
        # 將API內容寫入備份檔中
        tmpdata.to_csv(bakfile)
    # 回傳資料
    return tmpdata


# 取得價格與 TSE月營收
def getTSEPriceAndRevenue(prod, st, en):
    data1 = getDataFM(prod, st, en)
    st = st.replace("-", "")
    en = en.replace("-", "")
    data2 = getTSEMonthRevenue(prod, st, en)
    # 從每個月營收的資料 去抓出開高低收
    for i in range(1, data2.shape[0]):
        tmpdata = data1.loc[
            (data1.index > data2.index[i - 1]
             ) & (data1.index <= data2.index[i]),
        ]
        # 如果沒有資料
        if tmpdata.shape[0] == 0:
            # 移除資料
            continue
        data2.loc[data2.index[i],
                  "open"] = tmpdata.loc[tmpdata.index[0], "open"]
        data2.loc[data2.index[i], "high"] = tmpdata.loc[:, "high"].max()
        data2.loc[data2.index[i], "low"] = tmpdata.loc[:, "low"].min()
        data2.loc[data2.index[i],
                  "close"] = tmpdata.loc[tmpdata.index[-1], "close"]
        data2.loc[data2.index[i], "volume"] = tmpdata.loc[:, "volume"].sum()
    data2 = data2.drop_duplicates()
    return data2


# 取得價格與 FinMind 月營收
def getFMPriceAndRevenue(prod, st, en):
    data1 = getDataFM(prod, st, en)
    data2 = getFMMonthRevenue(prod, st, en)
    # 從每個月營收的資料 去抓出開高低收
    for i in range(1, data2.shape[0]):
        tmpdata = data1.loc[
            (data1.index > data2.index[i - 1]
             ) & (data1.index <= data2.index[i]),
        ]
        # 如果沒有資料
        if tmpdata.shape[0] == 0:
            # 移除資料
            continue
        data2.loc[data2.index[i],
                  "open"] = tmpdata.loc[tmpdata.index[0], "open"]
        data2.loc[data2.index[i], "high"] = tmpdata.loc[:, "high"].max()
        data2.loc[data2.index[i], "low"] = tmpdata.loc[:, "low"].min()
        data2.loc[data2.index[i],
                  "close"] = tmpdata.loc[tmpdata.index[-1], "close"]
        data2.loc[data2.index[i], "volume"] = tmpdata.loc[:, "volume"].sum()
    data2 = data2.dropna()
    return data2


# 取得價格、月營收、三大法人
def getPriceAndRevenueAndInstInvest(prod, st, en):
    a = getPriceAndInstInvest_FM(prod, st, en)
    st = st.replace("-", "")
    en = en.replace("-", "")
    b = getTSEMonthRevenue(prod, st, en)
    b["平均累計月營收成長率"] = b.rolling(12)["前期比較增減(%)"].mean()
    # 如果沒有月營收資料，則回傳價格資料
    if b.shape[0] == 0:
        return a
    for i in range(b.shape[0]):
        if i != b.shape[0] - 1:
            a.loc[
                (a.index > b.index[i]) & (
                    a.index <= b.index[i + 1]), "去年同月增減(%)"
            ] = b.loc[b.index[i], "去年同月增減(%)"]
            a.loc[
                (a.index > b.index[i]) & (
                    a.index <= b.index[i + 1]), "前期比較增減(%)"
            ] = b.loc[b.index[i], "前期比較增減(%)"]
            a.loc[
                (a.index > b.index[i]) & (
                    a.index <= b.index[i + 1]), "平均累計月營收成長率"
            ] = b.loc[b.index[i], "平均累計月營收成長率"]
        else:
            a.loc[(a.index > b.index[i]),
                  "去年同月增減(%)"] = b.loc[b.index[i], "去年同月增減(%)"]
            a.loc[(a.index > b.index[i]),
                  "前期比較增減(%)"] = b.loc[b.index[i], "前期比較增減(%)"]
            a.loc[(a.index > b.index[i]), "平均累計月營收成長率"] = b.loc[
                b.index[i], "平均累計月營收成長率"
            ]
    a = a[~a["去年同月增減(%)"].isna()]
    return a


# 取得所有股票商品代碼
def getStockList():
    # 備份檔名
    bakfile = f"{datapath}\\TSE_StockList.csv"
    # 檢視是否有該檔案存在
    if os.path.exists(bakfile):
        # 取得檔案內容
        df = pd.read_csv(bakfile)
    # 沒有的話就取檔案內容
    else:
        # 取得檔案內容
        res = requests.get(
            "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
        df = pd.read_html(res.text)[0]
        df.columns = df.iloc[0]
        df = df.iloc[2:]
        df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
        df.to_csv(bakfile)
    # 回傳資料
    return df
