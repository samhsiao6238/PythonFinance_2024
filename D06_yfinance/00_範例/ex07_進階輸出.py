"""
這個腳本必須使用 .py
pip install openpyxl
"""
import yfinance as yf
from ta.trend import MACD
from ta.momentum import StochasticOscillator

# 股票代碼
stock = "2331.TW"

# 下載資料
df = yf.download(tickers=stock, period="1d", interval="1m")

# 移動平均
df["MA5"] = df["Close"].rolling(window=5).mean()
df["MA20"] = df["Close"].rolling(window=20).mean()
macd = MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9)
stoch = StochasticOscillator(
    high=df["High"], close=df["Close"], low=df["Low"], window=14, smooth_window=3
)

# Add MACD and Stochastic Oscillator to the dataframe
df["MACD"] = macd.macd()
df["MACD_Signal"] = macd.macd_signal()
df["MACD_Diff"] = macd.macd_diff()
df["Stoch"] = stoch.stoch()
df["Stoch_Signal"] = stoch.stoch_signal()
# Remove timezone information from the datetime objects in the DataFrame
df.index = df.index.tz_localize(None)
# Save to an Excel file
excel_path = "stock_data.xlsx"
df.to_excel(excel_path)

print(excel_path)
