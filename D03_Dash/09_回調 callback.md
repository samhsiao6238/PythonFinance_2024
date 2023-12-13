# callback

簡單的 Dash 應用，透過下拉式選單更新圖表。

<br>

## 範例

1. 安裝庫

    ```bash
    pip install dash dash-core-components dash-html-components pandas
    ```

<br>

2. 完整程式碼

    ```python
    import dash
    from dash import dcc, html, Input, Output
    import plotly.express as px
    import pandas as pd

    # 準備一些範例數據
    df = pd.DataFrame({
        "Fruit": ["蘋果", "柳橙", "梨子", "香蕉"],
        "Amount": [4, 1, 2, 2],
        "City": ["SF", "SF", "Montreal", "Montreal"]
    })

    # 創建Dash應用
    app = dash.Dash(__name__)

    # 定義應用程式佈局
    app.layout = html.Div([
        dcc.Dropdown(
            id='city-dropdown',
            options=[{"label": city, "value": city} for city in df['City'].unique()],
            value='SF' # 預設值
        ),
        dcc.Graph(id='fruit-graph')
    ])

    # 定義callback來更新圖表
    @app.callback(
        Output('fruit-graph', 'figure'),
        Input('city-dropdown', 'value')
    )
    def update_graph(selected_city):
        # 根據選取的城市過濾數據
        filtered_df = df[df.City == selected_city]

        # 產生圖表
        fig = px.bar(filtered_df, x="Fruit", y="Amount", barmode="group")

        return fig

    # 運行應用
    if __name__ == '__main__':
        app.run_server(debug=True)
    ```

<br>

## 說明

1. 下拉式選單（`dcc.Dropdown`）。
2. 圖表（`dcc.Graph`）。
3. 裝飾器 `@callback`：定義回呼函數監聽下拉選單的值（`'city-dropdown'`的`value`屬性），並更新圖表（`'fruit-graph'`的`figure`屬性）。
4. 回呼函數 `update_graph`：根據下拉選單中選定的城市過濾數據，並產生相應的長條圖。

<br>

---

_END_