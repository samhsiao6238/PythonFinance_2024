# 從 dash 庫導入 Dash, dash_table, 和 html
# 修改
# from dash import Dash, dash_table, html
from dash import Dash, dcc, html, Input, Output

# 導入 pandas 庫
# import pandas as pd

# 導入 dash_core_components 和 dash_html_components
import dash_bootstrap_components as dbc

# 加入自訂模組
from components import geographical_content, content_classification


# 初始化一個 Dash 應用
# app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 定義應用的佈局：使用 HTML 的 Div 標籤來組織佈局
# app.layout = html.Div(
#     [
#         # 使用 H1 標籤顯示標題
#         html.H1("Netflix Movies and TV Shows Dashboard"),
#         # 使用水平線 (Hr 標籤) 分隔內容
#         html.Hr(),
#     ]
# )
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Netflix Movies and TV Shows Dashboard"),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Geographical content distribution", tab_id="tab1"
                ),
                dbc.Tab(label="Content classification", tab_id="tab2"),
            ],
            id="tabs",
            active_tab="tab1",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


# 加入回調
@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab1":
        return geographical_content.layout
    elif at == "tab2":
        return content_classification.layout


# 在本地開發模式下啟動 Dash 應用
# 檢查該腳本是否作為主程序運行
if __name__ == "__main__":
    # 運行伺服器，開啟 debug 模式以支持熱重新載入和錯誤日誌
    app.run_server(debug=True)
