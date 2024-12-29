'''導入庫'''
# 從 dash 庫導入 Dash, dcc, html 用於應用建立
from dash import Dash, dcc, html

# 導入 plotly.express 用於數據可視化
import plotly.express as px

# 導入 pandas 用於數據處理
import pandas as pd

# 導入 numpy 用於數值計算
import numpy as np

# 導入 dash_bootstrap_components 用於引入 Bootstrap 風格
import dash_bootstrap_components as dbc

'''模擬數據'''
'''
這裡說明一下，首先透過模擬的方式產生數據，然後把這個數據儲存為 EXCEL
透過觀察 EXCEL 可知道文件的內容，特過這樣的過程，
下一步可以試圖取得與 EXCEL 中的數據相同的內容來製圖
那這個腳本就會是一個相對完整的腳本了
'''
# 設置隨機種子
np.random.seed(0)
# 生成工作日的日期範圍
dates = pd.date_range("2020-01-01", "2023-05-31", freq="B")
# 生成投資組合價值的模擬數據
portfolio_values = np.random.normal(
    loc=0.0002, scale=0.001, size=len(dates)
).cumsum()
# 生成標準普爾 500 指數的模擬數據
snp_values = np.random.normal(
    loc=0.0001, scale=0.001, size=len(dates)
).cumsum()

# 建立 DataFrame 並進行整形處理
df_portfolio = pd.DataFrame(
    {"Date": dates, "Portfolio": portfolio_values, "S&P 500": snp_values}
)
# 測試觀察
df_portfolio.to_excel('portfolio_data_1.xlsx', index=False)
df_portfolio = df_portfolio.melt(
    id_vars="Date", var_name="Type", value_name="Value"
)

# 計算月度回報數據
monthly_return = (
    df_portfolio.groupby(
        [df_portfolio["Date"].dt.to_period("M"), "Type"]
    )["Value"]
    .last()
    .unstack()
)
# 測試觀察
monthly_return.to_excel('monthly_return_data_1.xlsx', index=True)
monthly_return = \
    monthly_return.pct_change().dropna().stack().reset_index(name="Return")
monthly_return["Date"] = monthly_return["Date"].dt.strftime("%Y-%m")

# 建立持股比例餅圖的數據
NUMBER = 10
top_holdings = pd.Series(
    np.random.rand(NUMBER), index=[f"Stock {i}" for i in range(1, NUMBER + 1)]
)
# 測試觀察
top_holdings.to_excel('top_holdings_1.xlsx')

'''儲存數據'''
# 儲存為 Excel
df_portfolio.to_excel('portfolio_data.xlsx', index=False)
monthly_return.to_excel('monthly_return_data.xlsx', index=False)

# 對於 Series 要先轉換為 DataFrame
top_holdings_df = pd.DataFrame(top_holdings, columns=['Value'])
top_holdings_df.to_excel('top_holdings_data.xlsx')

# 輸出結果
print("檔案儲存完畢。")

'''建立圖表'''
# 建立 Dash 應用，並使用 Bootstrap 主題
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 設置應用佈局
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                # 應用標題，透過 mt-4 設定 margin-top
                html.H1("Portfolio Dashboard", className="mt-4"),
                # 設置列寬 6 和偏移 3
                # width={"size": 6, "offset": 3},
                # 設置列寬為全寬
                width=12,
                # 文本居中類
                className="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    # 圖表 ID
                    id="portfolio-value-graph",
                    # 折線圖表
                    figure=px.line(
                        df_portfolio,
                        x="Date",
                        y="Value",
                        color="Type",
                        title="Total Portfolio Value ($USD)",
                    ),
                ),
                # 占滿整行
                width=12,
            )
        ),
        # 中間列
        dbc.Row(
            [
                # 佔滿柱狀圖
                dbc.Col(
                    dcc.Graph(
                        # 圖表 ID
                        id="monthly-return-graph",
                        # 柱狀圖表
                        figure=px.bar(
                            monthly_return,
                            x="Date",
                            y="Return",
                            color="Type",
                            title="Monthly Return (%)",
                        ),
                    ),
                    # 全部
                    width=12,
                )
            ]
        ),
        # 添加一個甜甜圈圖
        dbc.Row(
                [
                    # 左側餅圖
                    dbc.Col(
                        dcc.Graph(
                            # 圖表 ID
                            id="holdings-pie-chart",
                            # 餅圖表
                            figure=px.pie(
                                top_holdings,
                                values=top_holdings.values,
                                names=top_holdings.index,
                                title="Top X Holdings",
                            ),
                        ),
                        # 占一半行
                        width=6,
                    ),
                    # 右側甜甜圈圖
                    dbc.Col(
                        dcc.Graph(
                            id='holdings-donut-chart',
                            figure=px.pie(
                                top_holdings,
                                values=top_holdings.values,
                                names=top_holdings.index,
                                title="Top X Holdings",
                                # 添加這個 hole 參數就是一個甜甜圈圖
                                # 可通過更改數值來增加或減少中間空白的大小
                                hole=0.7
                            ),
                        ),
                        # 占一半行
                        width=6,
                    ),
                ]
        ),
        # 底部區塊
        dbc.Row(
            dbc.Col(
                html.P(
                    # 底部聲明
                    "Alert: this is not a actual portfolio.",
                    # 文本居中類
                    className="text-center",
                )
            )
        ),
    ],
    # 容器流體佈局
    fluid=True,
)

'''運行服務器'''
if __name__ == "__main__":
    # 開啟調試模式
    app.run_server(debug=True)
