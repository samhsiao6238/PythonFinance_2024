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

## 裝飾器結構

1. 程式碼。

    ```bash
    @app.callback(
        # 輸出：標籤與屬性
        Output("youbike-graph", "figure"),
        [
            # 輸入：標籤與屬性
            Input("area-dropdown", "value"),
            Input("bike-slider", "value")
        ],
    )
    ```

<br>

## 各個元素介紹
_這個過程中參與的角色_

1. 下拉式選單（`dcc.Dropdown`）。
2. 圖表（`dcc.Graph`）。
3. 裝飾器 `@callback`：定義回呼函數監聽下拉選單的值（`'city-dropdown'`的`value`屬性），並更新圖表（`'fruit-graph'`的`figure`屬性）。
4. 回呼函數 `update_graph`：根據下拉選單中選定的城市過濾數據，並產生相應的長條圖。

<br>

## 邏輯流程詳解

1. `@app.callback` 是一個裝飾器，可建立一個互動式功能，本質上是對指定的輸入進行監聽，並在監聽對象變動時，觸發回調函數處理數據，並進一步指定輸出來顯示變動後的數據一個函數。

<br>

2. `Input("area-dropdown", "value"), Input("bike-slider", "value")`：

    - 指定監聽的輸入
    - 當ID為`"area-dropdown"`的元件的`value`屬性（即下拉式選單的選取值）或ID為`"bike-slider"`的元件的`value`屬性（即滑桿的值）發生變化時，回呼函數將被觸發。

<br>

3. `def update_graph(selected_area, selected_bike_num)`：

    - 回調函數。
    - 函數的參數 `selected_area` 和 `selected_bike_num` 對應於兩個輸入元件的值（下拉式選單和滑桿），Dash 會將監聽對象變動後的值傳遞給回調函數的參數。

<br>

4. 函數內部的邏輯
    - 函數根據選取的區域（`selected_area`）和滑桿上的值（`selected_bike_num`）重新處理 `selected_df` DataFrame。
    - 使用 `plotly.express` 建立一個長條圖，顯示過濾後的資料。
    - 函數傳回一個 `figure` 對象，這個物件隨後被用於更新 `dcc.Graph` 元件。

<br>

5. `Output("youbike-graph", "figure")`：
    - 指定回呼函數的輸出目標。
    - 當回呼函數被觸發時，更新ID為`"youbike-graph"`的元件的`figure`屬性。
    - `figure` 就是圖表組件的 `dcc.Graph`。

<br>

---

_END_
