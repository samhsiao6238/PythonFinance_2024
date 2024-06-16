import matplotlib.pyplot as plt
import numpy_financial as npf
from Data import getMultipleReturn

# 在繪圖套件中載入中文字型
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False


# 計算單筆定額風險報酬
def RiskReturnRatio(data, price_column):

    # 計算年化報酬率 ( 總報酬率 ** (1/年份) -1 )
    returns = data[price_column].pct_change()
    ann_ret = (1 + returns).prod() ** (252 / returns.count()) - 1

    # 計算年化標準差
    # 日標準差 * (252**0.5)
    # 月標準差 * (12**0.5)
    ann_risk = returns.std() * (252 ** 0.5)

    # 計算夏普比率 ( 年化報酬 / 年化風險 )
    rf = 0.01
    ann_sharp = (ann_ret - rf) / ann_risk

    # 計算資產最大回落(%)
    dd = (1 + returns).cumprod() / (1 + returns).cumprod().cummax()
    mdd = (1 - dd).max()

    # 顯示評價函數
    print(f"起始時間: {data.index[0]} \n結束時間 {data.index[-1]}")
    print(f"年化報酬: {round(ann_ret, 3)}")
    print(f"年化標準差: {round(ann_risk, 3)}")
    print(f"年化夏普: {round(ann_sharp, 3)}")
    print(f"MDD: {round(mdd, 3)}")

    # 繪製權益曲線 以及回撤圖
    (1 + returns).cumprod().plot(label="累計報酬率曲線", legend=True)
    dd.plot(label="資產回撤曲線", legend=True)


# 計算定期定額報酬率以及繪製權益曲線圖
def ReturnRegularFixedInvestment(getDataFunction, symbol, price_column, once_amount):
    # 取得商品資料
    data = getDataFunction(symbol)
    data["ret"] = data[price_column].pct_change().copy()
    data["cap_ret"] = 1 + data["ret"].copy()

    # 將日期變成欄位 方便後續判斷
    data["today"] = data.index.copy()
    data["yesterday"] = data["today"].shift(1).copy()

    # 每個月投入金額
    inv_time = 0
    inv_action = []
    data = data.copy()
    for index, row in data.iterrows():
        # 換月定期定額投資
        if row["yesterday"].month != row["today"].month:
            data.loc[index, "inv_%s" % (inv_time)] = once_amount
            inv_time += 1
            inv_action.append(-once_amount)
    # 抓出定期定額的投資欄位 計算期末本金
    inv_col = [i for i in data.columns if i[:3] == "inv"]
    for col in inv_col:
        data[col].fillna(method="ffill", inplace=True)
        data[col] *= data.loc[data[col].notna(), "cap_ret"].iloc[1:].cumprod().copy()
    data["final_cap"] = data[inv_col].sum(axis=1).copy()

    # 計算內部報酬率
    inv_action.append(data["final_cap"].iloc[-1])

    # 顯示定期定額 細節
    print(f"起始時間: {data.index[0]}")
    print(f"結束時間: {data.index[-1]}")
    print(f"單次投入金額: {once_amount}")
    print(f"投入次數: {inv_time}")
    print(f"總投入本金: {once_amount * inv_time}")
    print(f"最後投資價值: {int(data['final_cap'].iloc[-1])}")
    print(f"每次投入的IRR:{round(npf.irr(inv_action) * 100, 2)}%")

    # 繪製權益曲線、回圖
    data["final_cap"].plot(label=f"{symbol}定期定額累計報酬率曲線", legend=True)
    (data["final_cap"] - data["final_cap"].cummax()).plot(
        label=f"{symbol}定期定額回撤曲線", legend=True
    )


# 多商品定期定額權益曲線
def MultipleReturnRegularFixedInvestment(
    getDataFunction, symbols, price_column, once_amount
):

    for symbol in symbols:
        print(f"商品程式碼 {symbol}")
        ReturnRegularFixedInvestment(
            getDataFunction, symbol, price_column, once_amount)
        plt.show()


# 資產配置風險報酬計算
def PortfolioRiskReturnRatio(getDataFunction, asset_allocation, price_column, cap):

    # 抓到所有歷史報酬率
    ret_dataframe = getMultipleReturn(
        getDataFunction, list(asset_allocation.keys()), price_column
    )
    ret_dataframe = ret_dataframe.dropna()
    print(ret_dataframe)

    # 年化風險報酬計算
    ann_ret = (ret_dataframe).prod() ** (252 / ret_dataframe.count()) - 1
    w = list(asset_allocation.values())
    weight_ann_ret = (ann_ret * w).sum()
    cov = (ret_dataframe).cov()
    weight_ann_risk = (
        cov.mul(asset_allocation, axis=0).mul(
            asset_allocation, axis=1).sum().sum()
    )

    # 顯示投資組合風險與報酬
    for key, value in asset_allocation.items():
        print(f"商品:{key} 權重:{value}")
    print(f"投資組合年化報酬:{weight_ann_ret}")
    print(f"投資組合風險:{weight_ann_risk}")

    # 資產配置 權益曲線計算
    cap_df = ret_dataframe.copy()
    cap_df["mix"] = 0
    for prod in asset_allocation.keys():
        # 計算單商品權益曲線
        cap_df[prod] = cap * (ret_dataframe[prod].cumprod())
        cap_df[prod].plot(label=f"{prod} 權益曲線", legend=True)
        # 分配資產比例
        cap_df["mix"] += cap_df[prod] * asset_allocation[prod]
    # 繪製資產配置的權益曲線圖
    cap_df["mix"].plot(label="資產配置權益曲線", legend=True)
