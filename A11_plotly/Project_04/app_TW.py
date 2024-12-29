# 將人口數量的隨機範圍改為台灣實際的人口數量範圍。
# 將地圖上的散點經緯度數據範圍改為台灣的經緯度範圍。
# 可以根據需要調整教育分布和收入分布數據。

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

# 設置隨機數生成的種子，以便每次生成的隨機數都相同
np.random.seed(0)

# 模擬台灣的人口數量和查詢時間
# 人口數量，隨機數在23000000到24000000之間
population_count = np.random.randint(23000000, 24000000)
# 查詢時間，隨機數在0.1到0.3秒之間
query_time = np.random.uniform(0.1, 0.3)

# 模擬台灣地圖上的散點經緯度數據
# 經度，隨機數在120到122之間
lon = np.random.uniform(120, 122, 1000)
# 緯度，隨機數在22到25之間
lat = np.random.uniform(22, 25, 1000)

# 建立一個DataFrame來儲存散點的經緯度和大小
df = pd.DataFrame(
    {
        "lat": lat, "lon": lon,
        "size": np.random.rand(1000) * 1000
    }
)

# 模擬教育分布和收入分布數據（這些分布可以根據實際數據進行調整）
education_distribution = pd.DataFrame(
    {
        "Education Level": np.random.choice(
            [
                "No Formal",
                "High School",
                "Associate Degree",
                "Bachelors",
                "Masters",
                "PhD",
            ],
            size=1000,
        ),
        "Count": np.random.randint(1, 100, size=1000),
    }
)

income_distribution = pd.DataFrame(
    {
        "Income Bracket": np.random.choice(
            [
                "<20k",
                "20k-40k",
                "40k-60k",
                "60k-80k",
                "80k-100k",
                ">100k"
            ], size=1000
        ),
        "Count": np.random.randint(1, 100, size=1000),
    }
)

# 建立Dash應用程序
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定義應用布局
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "台灣人口分佈",
                        className="text-center",
                    ),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="map",
                        figure=px.scatter_geo(
                            df,
                            lat="lat",
                            lon="lon",
                            size="size",
                            scope="asia",
                            center={"lat": 23.5, "lon": 121},
                            title="台灣人口分佈",
                        ).update_layout(
                            margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600
                        ),
                    ),
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="education-distribution",
                        figure=px.bar(
                            education_distribution,
                            x="Education Level",
                            y="Count",
                            title="台灣人口教育程度分佈",
                        ),
                    ),
                    width=6,
                ),
                dbc.Col(
                    dcc.Graph(
                        id="income-distribution",
                        figure=px.bar(
                            income_distribution,
                            x="Income Bracket",
                            y="Count",
                            title="台灣人口收入分佈",
                        ),
                    ),
                    width=6,
                ),
            ]
        ),
    ],
)

# 啟動應用程序
if __name__ == "__main__":
    app.run_server(debug=True)
