# 導入 pandas 庫
import pandas as pd

# 導入 plotly express 庫，用於製作圖表
import plotly.express as px

# 從 dash 庫導入 dcc 和 html
from dash import dcc, html

# 讀取 Netflix 標題數據
df = pd.read_csv("netflix_titles.csv")

# 分割 listed_in 列並展開以處理多個類型
# 將 listed_in 列的每個項目分割為列表
df["listed_in"] = df["listed_in"].str.split(", ")
# 將列表展開成多行
df = df.explode("listed_in")

# 計算每種類型和類型組合的數量
df_counts = df.groupby(["type", "listed_in"]).size().reset_index(name="count")

# 建立樹形圖來顯示不同類型和類型的內容
fig = px.treemap(
    df_counts,
    path=["type", "listed_in"],
    values="count",
    color="count",
    color_continuous_scale="Ice",
    title="Content by type and genre",
)

# 更新圖表的佈局設置
fig.update_layout(width=1280, height=960, title_x=0.5)
# 更新圖表痕跡的文本信息和字體大小
fig.update_traces(textinfo="label+percent entry", textfont_size=14)

# 定義 Dash 應用的佈局
layout = html.Div(
    [
        # 將圖表添加到 Dash 應用的佈局中
        dcc.Graph(figure=fig),
    ]
)
