from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# 模拟一些数据
np.random.seed(0)
dates = pd.date_range("2020-01-01", "2021-05-31", freq="B")
portfolio_values = np.random.normal(loc=0.0002, scale=0.001, size=len(dates)).cumsum()
snp_values = np.random.normal(loc=0.0001, scale=0.001, size=len(dates)).cumsum()

df_portfolio = pd.DataFrame(
    {"Date": dates, "Portfolio": portfolio_values, "S&P 500": snp_values}
)
df_portfolio = df_portfolio.melt(id_vars="Date", var_name="Type", value_name="Value")

# 用于月度回报的数据
monthly_return = (
    df_portfolio.groupby([df_portfolio["Date"].dt.to_period("M"), "Type"])["Value"]
    .last()
    .unstack()
)
monthly_return = monthly_return.pct_change().dropna().stack().reset_index(name="Return")
monthly_return["Date"] = monthly_return["Date"].dt.strftime("%Y-%m")

# 持股比例饼图的数据
top_holdings = pd.Series(
    np.random.rand(15), index=[f"Stock {i}" for i in range(1, 16)]
)

# 创建 Dash 应用
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 设置应用布局
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Portfolio Dashboard"),
                width={"size": 6, "offset": 3},
                className="text-center",
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="portfolio-value-graph",
                    figure=px.line(
                        df_portfolio,
                        x="Date",
                        y="Value",
                        color="Type",
                        title="Total Portfolio Value ($USD)",
                    ),
                ),
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="monthly-return-graph",
                        figure=px.bar(
                            monthly_return,
                            x="Date",
                            y="Return",
                            color="Type",
                            title="Monthly Return (%)",
                        ),
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        id="holdings-pie-chart",
                        figure=px.pie(
                            top_holdings,
                            values=top_holdings.values,
                            names=top_holdings.index,
                            title="Top 15 Holdings",
                        ),
                    ),
                    width=6,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    "Spoiler alert: this is not my actual portfolio!",
                    className="text-center",
                )
            )
        ),
    ],
    fluid=True,
)

# 运行服务器
if __name__ == "__main__":
    app.run_server(debug=True)
