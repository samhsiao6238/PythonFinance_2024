import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Simulate some data
date_rng = pd.date_range(start="2020-01-01", end="2020-01-30", freq="D")
data = pd.DataFrame(date_rng, columns=["date"])
data["open"] = np.random.uniform(low=100, high=200, size=(len(date_rng)))
data["high"] = data["open"] + np.random.uniform(low=1, high=10, size=(len(date_rng)))
data["low"] = data["open"] - np.random.uniform(low=1, high=10, size=(len(date_rng)))
data["close"] = np.random.uniform(low=100, high=200, size=(len(date_rng)))
data["volume"] = np.random.randint(100, 1000, size=(len(date_rng)))

# Create a candlestick chart
fig = go.Figure(
    data=[
        go.Candlestick(
            x=data["date"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
        )
    ]
)

fig.update_layout(title="Mock Trading Data", xaxis_title="Date", yaxis_title="Price")

fig.show()

# To export to Excel:
data.to_excel("trading_data.xlsx")
