import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np


# 模擬數據生成
np.random.seed(0)
batch_numbers = np.arange(1, 31)
control_chart_data = np.random.rand(30) * 0.1
control_chart_limits = [0.08, 0.02]

# 創建 Dash 應用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 應用佈局
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            dbc.Col(
                html.H1(
                    "CONTROL CHARTS DASHBOARD",
                    className="text-center text-primary mt-4",
                ),
                width=12,
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="process-control-chart",
                        figure={
                            "data": [
                                go.Scatter(
                                    x=batch_numbers,
                                    y=control_chart_data,
                                    mode="lines+markers",
                                )
                            ],
                            "layout": go.Layout(
                                title="Live SPC Chart",
                                xaxis={"title": "Batch Number"},
                                yaxis={"title": "Value"},
                                shapes=[
                                    {
                                        "type": "line",
                                        "y0": control_chart_limits[0],
                                        "y1": control_chart_limits[0],
                                        "x0": 0,
                                        "x1": batch_numbers[-1],
                                        "line": {"color": "red", "width": 2},
                                    },
                                    {
                                        "type": "line",
                                        "y0": control_chart_limits[1],
                                        "y1": control_chart_limits[1],
                                        "x0": 0,
                                        "x1": batch_numbers[-1],
                                        "line": {"color": "red", "width": 2},
                                    },
                                ],
                            ),
                        },
                    ),
                    width=12,
                )
            ]
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
