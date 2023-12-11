# 使用 .py
# 導入庫
# ta
from ta.trend import MACD
from ta.momentum import StochasticOscillator

# 導入市場數據庫
import yfinance as yf

# 數據可視化
import plotly
import plotly.graph_objs as go


# 覆蓋 Yahoo Finance 的默認設置
yf.pdr_override()

# 輸入股票代號進行查詢
stock = input("Enter a stock ticker symbol: ")

# 從 yfinance API 獲取股票數據
df = yf.download(tickers=stock, period="1d", interval="1m")

#  計算 5 日和 20 日移動平均線
df["MA5"] = df["Close"].rolling(window=5).mean()
df["MA20"] = df["Close"].rolling(window=20).mean()

# 計算 MACD 指標
macd = MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9)

# 計算隨機振盪器
stoch = StochasticOscillator(
    high=df["High"], close=df["Close"],
    low=df["Low"], window=14, smooth_window=3
)

# 初始化 plotly 圖形
fig = go.Figure()

# 創建含有多個子圖的圖形
fig = plotly.subplots.make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.01,
    row_heights=[0.5, 0.1, 0.2, 0.2],
)

# 在第一行添加蠟燭圖
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="market data",
    )
)

# 在第一行添加移動平均線
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA5"],
        opacity=0.7,
        line=dict(color="blue", width=2),
        name="MA 5",
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA20"],
        opacity=0.7,
        line=dict(color="orange", width=2),
        name="MA 20",
    )
)

# 在第二行添加成交量柱狀圖
colors = [
    "green" if row["Open"] - row["Close"] >= 0 else "red"
    for index, row in df.iterrows()
]
fig.add_trace(
    go.Bar(x=df.index, y=df["Volume"], marker_color=colors), row=2, col=1
)

# 在第三行添加 MACD 指標圖
colorsM = ["green" if val >= 0 else "red" for val in macd.macd_diff()]
fig.add_trace(
    go.Bar(x=df.index, y=macd.macd_diff(), marker_color=colorsM), row=3, col=1
)
fig.add_trace(
    go.Scatter(x=df.index, y=macd.macd(), line=dict(color="black", width=2)),
    row=3,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df.index, y=macd.macd_signal(),
        line=dict(color="blue", width=1)
    ),
    row=3,
    col=1,
)

# Plot stochastics trace on 4th row
fig.add_trace(
    go.Scatter(
        x=df.index, y=stoch.stoch(), line=dict(color="black", width=2)
    ),
    row=4,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df.index, y=stoch.stoch_signal(), line=dict(color="blue", width=1)
    ),
    row=4,
    col=1,
)

# 透過更改繪圖大小、隱藏圖例和範圍滑桿以及消除日期之間的間隙來更新佈局
fig.update_layout(
    height=900, width=1200, showlegend=False, xaxis_rangeslider_visible=False
)


# 使標題動態化以反映我們正在分析的股票
fig.update_layout(
    title=str(stock) + " Live Share Price:",
    yaxis_title="Stock Price (USD per Shares)"
)

# 更新 y 軸標籤
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)
fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)
fig.update_yaxes(title_text="Stoch", row=4, col=1)

fig.update_xaxes(
    rangeslider_visible=False,
    rangeselector_visible=False,
    rangeselector=dict(
        buttons=list(
            [
                dict(
                    count=15, label="15m", step="minute", stepmode="backward"
                ),
                dict(
                    count=45, label="45m", step="minute", stepmode="backward"
                ),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all"),
            ]
        )
    ),
)

fig.show()
