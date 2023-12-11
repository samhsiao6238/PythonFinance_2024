import plotly.graph_objects as go
import pandas as pd
from dash import Dash, dcc, html

# 地圖代碼
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv")

colors = ["rgb(239,243,255)", "rgb(189,215,231)", "rgb(107,174,214)", "rgb(33,113,181)"]
months = {6: "June", 7: "July", 8: "Aug", 9: "Sept"}

fig = go.Figure()

for i in range(6, 10)[::-1]:
    df_month = df.query("Month == %d" % i)
    fig.add_trace(
        go.Scattergeo(
            lon=df_month["Lon"],
            lat=df_month["Lat"],
            text=df_month["Value"],
            name=months[i],
            marker=dict(size=df_month["Value"] / 50, color=colors[i - 6], line_width=0),
        )
    )

df_sept = df.query("Month == 9")
fig["data"][0].update(
    mode="markers+text",
    textposition="bottom center",
    text=df_sept["Value"].map("{:.0f}".format).astype(str) + " " + df_sept["Country"],
)

fig.add_trace(
    go.Choropleth(
        locationmode="country names",
        locations=df_sept["Country"],
        z=df_sept["Value"],
        text=df_sept["Country"],
        colorscale=[[0, "rgb(0, 0, 0)"], [1, "rgb(0, 0, 0)"]],
        autocolorscale=False,
        showscale=False,
        geo="geo2",
    )
)
fig.add_trace(
    go.Scattergeo(
        lon=[21.0936],
        lat=[7.1881],
        text=["Africa"],
        mode="text",
        showlegend=False,
        geo="geo2",
    )
)

fig.update_layout(
    title=go.layout.Title(
        text='Ebola cases reported by month in West Africa 2014<br> \
Source: <a href="https://data.hdx.rwlabs.org/dataset/rowca-ebola-cases">HDX</a>'
    ),
    geo=go.layout.Geo(
        resolution=50,
        scope="africa",
        showframe=False,
        showcoastlines=True,
        landcolor="rgb(229, 229, 229)",
        countrycolor="white",
        coastlinecolor="white",
        projection_type="mercator",
        lonaxis_range=[-15.0, -5.0],
        lataxis_range=[0.0, 12.0],
        domain=dict(x=[0, 1], y=[0, 1]),
    ),
    geo2=go.layout.Geo(
        scope="africa",
        showframe=False,
        landcolor="rgb(229, 229, 229)",
        showcountries=False,
        domain=dict(x=[0, 0.6], y=[0, 0.6]),
        bgcolor="rgba(255, 255, 255, 0.0)",
    ),
    legend_traceorder="reversed",
)

# Dash 應用程序代碼
app = Dash()
app.layout = html.Div([dcc.Graph(figure=fig)])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
