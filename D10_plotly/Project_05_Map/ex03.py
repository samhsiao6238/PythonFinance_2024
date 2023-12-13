"""
Bubble Map with go.Scattergeo
"""
import plotly.graph_objects as go

import pandas as pd
import requests
import sys


# 資料檔案 URL
url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv"

# 發送 GET 請求
response = requests.get(url)

# 檢查並下載
if response.status_code == 200:
    # 檔案名稱
    file_path = "2014_us_cities.csv"

    # 儲存檔案
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"檔案完成下載 {file_path}")
else:
    print("檔案下載失敗")
    # 退出
    sys.exit(1)


# 讀取檔案
df = pd.read_csv("2014_us_cities.csv")

# 也可以直接從雲端讀取檔案
# df = pd.read_csv(
#     "https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv"
# )

df.head()

df["text"] = df["name"] + "<br>Population " + \
    (df["pop"] / 1e6).astype(str) + " million"
limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]
colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
cities = []
scale = 5000

fig = go.Figure()

for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]: lim[1]]
    fig.add_trace(
        go.Scattergeo(
            locationmode="USA-states",
            lon=df_sub["lon"],
            lat=df_sub["lat"],
            text=df_sub["text"],
            marker=dict(
                size=df_sub["pop"] / scale,
                color=colors[i],
                line_color="rgb(40,40,40)",
                line_width=0.5,
                sizemode="area",
            ),
            name="{0} - {1}".format(lim[0], lim[1]),
        )
    )

fig.update_layout(
    title_text='''
        2014 US city populations<br>(
        Click legend to toggle traces)
    ''',
    showlegend=True,
    geo=dict(
        scope="usa",
        landcolor="rgb(217, 217, 217)",
    ),
)

fig.show()
