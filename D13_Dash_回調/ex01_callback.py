import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 模擬數據
df = pd.DataFrame(
    {
        "Fruit": ["蘋果", "柳橙", "梨子", "香蕉"],
        "Amount": [40, 13, 25, 28],
        "City": ["城市A", "城市C", "城市B", "城市C"],
    }
)

# 建立 Dash 應用
app = dash.Dash(__name__)

# 定義佈局
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="city-dropdown",
            options=[
                {"label": city, "value": city} for city in df["City"].unique()
            ],
            # 預設值
            value="SF",
        ),
        dcc.Graph(id="fruit-graph"),
    ]
)


# 定義callback來更新圖表
@app.callback(Output("fruit-graph", "figure"), Input("city-dropdown", "value"))
def update_graph(selected_city):
    # 根據選取的城市過濾數據
    filtered_df = df[df.City == selected_city]

    # 產生圖表
    fig = px.bar(filtered_df, x="Fruit", y="Amount", barmode="group")

    return fig


# 運行應用
if __name__ == "__main__":
    app.run_server(debug=True)
