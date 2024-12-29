import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# 模擬 180 天的交易數據
num_days = 180
dates = pd.date_range(
    start=datetime.today() - pd.to_timedelta(num_days, unit="D"),
    periods=num_days
)

# 初始化開盤價格為100，並讓後續開盤價格等於前一日的收盤價格
opens = [100] + [0] * (num_days - 1)
for i in range(1, num_days):
    # 模擬前一日收盤價格的波動
    opens[i] = opens[i - 1] + np.random.uniform(-1.5, 1.5)
# 確保最高價格高於開盤價格
highs = [o + np.random.uniform(0, 2) for o in opens]
# 確保最低價格低於開盤價格
lows = [o - np.random.uniform(0, 2) for o in opens]
closes = [
    l + np.random.uniform(0, (h - l)) for h, l in zip(highs, lows)
]  # 收盤價格在最高和最低之間
volumes = np.random.randint(100000, 200000, num_days)

# 建立 DataFrame
df = pd.DataFrame(
    {
        "Date": dates,
        "Open": opens,
        "High": highs,
        "Low": lows,
        "Close": closes,
        "Volume": volumes,
    }
)

# 將 DataFrame 保存為 Excel 文件
excel_path = "simulated_trading_data.xlsx"
df.to_excel(excel_path, index=False)


# 计算 RSI
def compute_rsi(dataframe, column="Close", period=14):
    delta = dataframe[column].diff()
    gain = (delta > 0) * delta
    loss = (delta < 0) * -delta

    average_gain = gain.rolling(window=period).mean()
    average_loss = loss.rolling(window=period).mean()

    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# 计算 MACD 和 Signal Line
def compute_macd(
    dataframe, column="Close", fast_period=12, slow_period=26, signal_period=9
):
    fast_ema = dataframe[column].ewm(span=fast_period, adjust=False).mean()
    slow_ema = dataframe[column].ewm(span=slow_period, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal_line


# 计算 Stochastic Oscillator
def compute_stochastic_oscillator(
    dataframe,
    high_col="High",
    low_col="Low",
    close_col="Close",
    k_period=14,
    d_period=3,
):
    low_min = dataframe[low_col].rolling(window=k_period).min()
    high_max = dataframe[high_col].rolling(window=k_period).max()
    k_line = ((dataframe[close_col] - low_min) / (high_max - low_min)) * 100
    d_line = k_line.rolling(window=d_period).mean()
    return k_line, d_line


# 将计算得到的技术指标添加到数据框中
df["RSI"] = compute_rsi(df)
df["MACD"], df["Signal_Line"] = compute_macd(df)
df["K"], df["D"] = compute_stochastic_oscillator(df)

# 创建子图对象，指定每个子图的类型
fig = make_subplots(
    rows=4,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,  # 调整子图之间的垂直间距
    subplot_titles=(
        "Candlestick", "RSI", "Volume and MACD", "Stochastic Oscillator"
    ),
    specs=[
        # 指定第一行是蠟燭圖
        [{"type": "candlestick"}],
        # 指定第二行是折線圖
        [{"type": "scatter"}],
        # 指定第三行是柱狀圖，但也可以包含折線圖
        [{"type": "bar"}],
        # 指定第四行也是折線圖
        [{"type": "scatter"}],
    ],
)

# 添加蠟燭圖
fig.add_trace(
    go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        showlegend=False,
    ),
    row=1,
    col=1,
)

# 添加 RSI 折线图
fig.add_trace(
    go.Scatter(
        x=df["Date"], y=df["RSI"], name="RSI", mode="lines"
    ), row=2, col=1
)

# 添加 Volume 和 MACD 柱状图和折线图
fig.add_trace(
    go.Bar(
        x=df["Date"], y=df["Volume"], name="Volume"
    ), row=3, col=1
)
fig.add_trace(
    go.Scatter(
        x=df["Date"], y=df["MACD"], name="MACD",
        mode="lines",
        line=dict(color="blue")
    ),
    row=3,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Signal_Line"],
        name="Signal Line",
        mode="lines",
        line=dict(color="orange"),
    ),
    row=3,
    col=1,
)

# 添加 Stochastic Oscillator 折线图
fig.add_trace(
    go.Scatter(
        x=df["Date"], y=df["K"], name="K Line", mode="lines"
    ), row=4, col=1
)
fig.add_trace(
    go.Scatter(
        x=df["Date"], y=df["D"], name="D Line", mode="lines"
    ), row=4, col=1
)

# 更新图表布局，使其展开至全屏
fig.update_layout(
    # 自动调整大小
    autosize=True,
    # 调整图表的外边距
    margin=dict(l=50, r=50, b=100, t=100, pad=4),
    showlegend=False,
    title_text="Simulated Trading Data Charts",
    # 隐藏范围滑块
    xaxis_rangeslider_visible=False,
)
# 显示图表
fig.show()
