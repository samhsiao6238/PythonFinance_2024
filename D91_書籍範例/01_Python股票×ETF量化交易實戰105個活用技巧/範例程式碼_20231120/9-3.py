# 載入必要套件
from BackTest import ChartTrade
import mplfinance as mpf
import pandas as pd
import os
import yfinance as yf


# 設定在根目錄即可，之後可以改到 /data
datapath = "./"


# 更新資料源為 yahoo finance
def getDataFM(prod, st, en):
    #
    bakfile = f"data//YF_{prod}_{st}_{en}_stock_daily_adj.csv"
    if os.path.exists(bakfile):
        data = pd.read_csv(bakfile)
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.set_index("Date")
    else:
        data = yf.download(f"{prod}.TW", start=st, end=en)
        data.columns = [i.lower() for i in data.columns]
        # 除錯 如果沒有資料
        if data.shape[0] == 0:
            print("沒有資料")
            return pd.DataFrame()
        # 將資料寫入備份檔
        data.to_csv(bakfile)
    return data


# 取得三大法人 證交所資料來源
def getTSEInstitutionalInvestors(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}//{prod}_{st}_{en}_TSE_InstitutionalInvestorsBuySell.csv"
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
        tmpdata = pd.read_csv("三大法人爬蟲資料.csv", encoding="utf-8")
        tmpdata = tmpdata[
            (tmpdata["證券代號"] == prod) &
            (tmpdata["日期"] >= int(st)) &
            (tmpdata["日期"] <= int(en))
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


# 取得股價以及融資融券 證交所資料來源
def getTSEPriceAndMarginTrade(prod, st, en):
    data1 = getDataFM(prod, st, en)
    print('===========1============')
    print(data1.head(3))
    # 取得證交所的融資融券
    st = st.replace("-", "")
    en = en.replace("-", "")
    data2 = getTSEMarginTrading(prod, st, en)
    print('===========2============')
    print(data2.head(3))
    data3 = pd.concat([data1, data2], axis=1, join="inner")
    print('===========3============')
    print(data3.head(3))
    return data3


# 取得融資融券 證交所資料來源
def getTSEMarginTrading(prod, st, en):
    # 備份檔名
    bakfile = f"{datapath}/{prod}_{st}_{en}_TSE_MarginTrading.csv"
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
        tmpdata = pd.read_csv("融資融券爬蟲資料.csv", encoding="utf-8")
        tmpdata = tmpdata[
            (tmpdata["股票代號"] == prod) &
            (tmpdata["日期"] >= int(st)) &
            (tmpdata["日期"] <= int(en))
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
    print('===========4============')
    print(tmpdata.head(3))
    return tmpdata


# 取得回測資料
prod = "2330"
data = getTSEPriceAndMarginTrade(prod, "2023-09-01", "2023-12-10")
# 這是查看欄位名稱使用
# print(data.columns)
print(data.head(10))
# 融資融券餘額
data["融券今日餘額"] = data["融券今日餘額"].astype(int)
data["融資今日餘額"] = data["融資今日餘額"].astype(int)

# 計算券資比
data["券資比"] = data["融券今日餘額"] / data["融資今日餘額"]

print(data.head(10))

# # 繪製副圖
# addp = []
# # 融資融券
# addp.append(mpf.make_addplot(data["融資今日餘額"], panel=1, color="red", secondary_y=False))
# addp.append(mpf.make_addplot(data["融券今日餘額"], panel=2, color="red", secondary_y=False))
# addp.append(mpf.make_addplot(data["券資比"], panel=3, color="red", secondary_y=False))

# # 繪製K線圖與交易明細
# ChartTrade(data, addp=addp, v_enable=False)
