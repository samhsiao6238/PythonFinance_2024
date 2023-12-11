import pandas as pd  # 導入 pandas 庫
import plotly.express as px  # 導入 plotly express 用於製作圖表
from dash import dcc, html  # 從 dash 庫導入 dcc 和 html

df = pd.read_csv("netflix_titles.csv")  # 讀取 Netflix 標題數據

# 過濾掉沒有國家信息的條目，如果有多個製作國家，則以第一個國家作為製作國家
df["country"] = (
    df["country"]
    .str.split(",")
    .apply(lambda x: x[0].strip() if isinstance(x, list) else None)
)

# 從 date_added 列提取年份
df["year_added"] = pd.to_datetime(df["date_added"]).dt.year
# 刪除 country 和 year_added 列中有缺失值的行
df = df.dropna(subset=["country", "year_added"])

# 計算每個國家每年製作的內容數量
df_counts = df.groupby(
    ["country", "year_added"]
).size().reset_index(name="count")

# 按 'year_added' 排序，確保動畫幀按升序排列
df_counts = df_counts.sort_values("year_added")

# 創建地圖，包含年份的滑動條
fig1 = px.choropleth(
    df_counts,
    locations="country",
    locationmode="country names",
    color="count",
    hover_name="country",
    animation_frame="year_added",
    projection="natural earth",
    title="Content produced by countries over the years",
    color_continuous_scale="YlGnBu",
    range_color=[0, df_counts["count"].max()],
)
fig1.update_layout(width=1280, height=720, title_x=0.5)  # 更新佈局設置

# 計算每年按類型製作的內容數量，並為缺失的類型-年份對填充零
df_year_counts = df.groupby(["year_added", "type"]).size().reset_index(name="count")

# 使用 plotly express 創建折線圖
fig2 = px.line(
    df_year_counts,
    x="year_added",
    y="count",
    color="type",
    title="Content distribution by type over the years",
    markers=True,
    color_discrete_map={"Movie": "dodgerblue", "TV Show": "darkblue"},
)
fig2.update_traces(marker=dict(size=12))  # 更新線條的跟踪器設置
fig2.update_layout(width=1280, height=720, title_x=0.5)  # 更新佈局設置

# 定義 dash 的佈局
layout = html.Div(
    [
        dcc.Graph(figure=fig1),  # 添加地圖圖表
        html.Hr(),  # 添加水平分隔線
        dcc.Graph(figure=fig2),  # 添加折線圖
    ]
)
