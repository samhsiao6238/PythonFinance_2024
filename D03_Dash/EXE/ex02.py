import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests

# 你的程式碼來取得和處理數據
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    column_mapping = {
        "sno": "站點編號",
        "sna": "站點名稱",
        "tot": "車位總數",
        "sbi": "可借車數",
        "sarea": "所在區域",
        "mday": "資料更新時間",
        "lat": "緯度",
        "lng": "經度",
        "ar": "地址",
        "sareaen": "區域英文名稱",
        "snaen": "站點英文名稱",
        "aren": "地址英文",
        "bemp": "空位數量",
        "act": "啟用狀態",
        "srcUpdateTime": "來源更新時間",
        "updateTime": "更新時間",
        "infoTime": "訊息時間",
        "infoDate": "訊息日期",
    }
    df.rename(columns=column_mapping, inplace=True)
    selected_df = df[["站點名稱", "車位總數", "可借車數", "所在區域"]]
else:
    print("無法下載數據，狀態碼：", response.status_code)


# 可添加一些運算取得數據，然後
# 中位數
median_bike_num = selected_df["可借車數"].median()
# 最大數值的一半
half_max_bike_num = selected_df["可借車數"].max() / 2

# 建立 Dash 應用
app = dash.Dash(__name__)

# 定義佈局
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="area-dropdown",
            options=[
                {"label": area, "value": area} for area in selected_df["所在區域"].unique()
            ],
            # 預設值
            value=selected_df["所在區域"].unique()[0],
        ),
        dcc.Slider(
            id="bike-slider",
            min=selected_df["可借車數"].min(),
            max=selected_df["可借車數"].max(),
            # value=selected_df["可借車數"].max(),
            value=10,
            marks={
                i: str(i)
                for i in range(selected_df["可借車數"].min(), selected_df["可借車數"].max() + 1)
            },
            step=1,
        ),
        dcc.Graph(id="youbike-graph"),
    ]
)


# 定義callback來更新圖表
@app.callback(
    Output("youbike-graph", "figure"),
    [Input("area-dropdown", "value"), Input("bike-slider", "value")],
)
def update_graph(selected_area, selected_bike_num):
    # 根據所選的區域和滑塊範圍過濾數據
    filtered_df = selected_df[
        (selected_df["所在區域"] == selected_area)
        & (selected_df["可借車數"] >= selected_bike_num)
    ]

    # 產生圖表
    fig = px.bar(
        filtered_df, x="站點名稱", y=["車位總數", "可借車數"], barmode="group", title="YouBike站點數據"
    )

    return fig


# 運行應用
if __name__ == "__main__":
    app.run_server(debug=True)
