import streamlit as st
import pandas as pd
import datetime as dt
import altair as alt
import requests
import folium
import plotly.graph_objects as go
from folium.plugins import MousePosition
from st_aggrid import (
    AgGrid,
    ColumnsAutoSizeMode,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
)


def load_lottieurl(url) -> dict:

    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def set_dataset_size(df: pd.DataFrame, size: str) -> pd.DataFrame:
    """
    Limits dataset to 30 days, 7 days or 24 hours time periods.
    Returns filtered dataframe.
    """

    # df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format='%d-%b-%Y %H:%M:%S')
    # Removing timezone info
    df["time (UTC)"] = pd.to_datetime(
        df["time (UTC)"], infer_datetime_format=True
    ).dt.tz_localize(None)

    max_time = df["time (UTC)"].max()
    min_time = max_time - dt.timedelta(days=size)

    df = df.loc[(df["time (UTC)"] >= min_time) & (df["time (UTC)"] <= max_time)]

    return df


# 篩選數據
def data_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Updates ag-Grid table and map according to selected filters.
    Returns filtered dataframe.
    """

    filter_container = st.container()

    with filter_container:

        filter_col1, filter_col2 = st.columns((1, 1))
        with filter_col1:
            periodicals = {
                "Past 30 Days": 30,
                "Past 7 Days": 7,
                "Last 24 Hours": 1
            }
            option = st.selectbox(
                label="Dataset size",
                options=periodicals.keys(),
            )

            df = set_dataset_size(df, periodicals[option])

        # 修改以腳本，原本的 source 面板並未被使用到而會出現警告
        # 這部分僅顯示資料來源沒有其他用途
        with filter_col2:
            # 假設有多個資料來源可選擇時可修改列表
            source_options = ["United States Geological Survey"]
            #
            source = st.selectbox(
                label="Dataset source",
                options=source_options,
                disabled=False,
            )
        # 使用選擇的數據來過濾 DataFrame
        if 'source' in df.columns:
            df = df[df['source'] == source]

        # If not selected, funtion will return dataframe before applying additional filters
        add_filter = st.checkbox("Add more filters")
        if not add_filter:
            return df

        # FILTERING DATAFRAME
        selected_columns = st.multiselect(
            "Choose an option to filter dataframe",
            df.loc[:, df.columns != "place"].columns,
        )

        for column in selected_columns:
            left, right = st.columns((1, 20))

            if column == "time (UTC)":
                if len(df) > 0:
                    date_col1, date_col2, date_col3, date_col4 = st.columns(
                        (1, 4.4, 4.4, 10)
                    )

                    start_dt = date_col2.date_input(
                        "➤ Start date", value=df["time (UTC)"].min()
                    )
                    end_dt = date_col3.date_input(
                        "➤ End date", value=df["time (UTC)"].max()
                    )

                    if start_dt <= end_dt:
                        df = df.loc[
                            (
                                df["time (UTC)"] >= dt.datetime(
                                    start_dt.year, start_dt.month, start_dt.day
                                )
                            ) & (
                                df["time (UTC)"] <= dt.datetime(
                                    end_dt.year, end_dt.month, end_dt.day
                                ) + dt.timedelta(days=1)
                            )
                        ]
                    else:
                        date_col2.warning("Please check your date range")
                else:
                    right.error(f"Not enough {column} values to filter")

            elif column in ["latitude", "longitude"]:
                if column == "latitude":
                    min_coordinate = -90
                    max_coordinate = 90
                elif column == "longitude":
                    min_coordinate = -180
                    max_coordinate = 180

                coordinate_input = right.slider(
                    f"➤ Select your {column} range",
                    min_value=min_coordinate,
                    max_value=max_coordinate,
                    value=(min_coordinate, max_coordinate),
                )

                df = df.loc[df[column].between(*coordinate_input)]

            elif column in ["depth", "mag"]:
                if len(df) > 1:
                    min_value = float(df[column].min())
                    max_value = float(df[column].max())

                    if min_value == max_value:
                        right.warning(
                            f"{column.capitalize()} value is same for all rows"
                        )

                    else:
                        value_range = right.slider(
                            f"➤ Select your {column} range",
                            min_value=min_value,
                            max_value=max_value,
                            value=(min_value, max_value),
                            help=f"You can limit minimum and maximum {column} values via sliders. This will update your table.",
                        )

                        df = df.loc[df[column].between(*value_range)]
                else:
                    right.error(f"Not enough {column} values to filter")

            elif column in ["magType", "type", "locationSource", "magSource", "status"]:
                if len(df) > 0:
                    category_input = right.multiselect(
                        f"➤ Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                    )

                    df = df.loc[df[column].isin(category_input)]
                else:
                    right.error(f"Not enough {column} values to filter")

        return df


def convert_to_csv(df):
    """Converts filtered pandas dataframe to CSV file"""

    return df.to_csv(index=False, encoding="utf-8")


def create_data_grid(df: pd.DataFrame) -> list:
    """Creates ag-Grid data grid with filtered data and returns list of selected rows"""

    grid = GridOptionsBuilder.from_dataframe(df)
    # Separating grid into discrete pages instead of scrolling
    grid.configure_pagination(enabled=True)
    # Selection checkboxes on the grid
    grid.configure_selection(
        selection_mode="multiple", header_checkbox=True, use_checkbox=True
    )
    # Changing cell style for magnitude values over or equal to 6
    cellsytle_jscode = JsCode(
        """
    function(params) {
        if (params.value >= 7) {
            return {
                'color': 'white',
                'backgroundColor': 'firebrick'
            };
        } else if (params.value >= 6) {
            return {
                'color': 'white',
                'backgroundColor': 'chocolate'
            };
        } else if (params.value >= 5) {
            return {
                'color': 'white',
                'backgroundColor': 'olivedrab'
            };
        }
    };
    """
    )

    grid.configure_column("mag", cellStyle=cellsytle_jscode)

    grid.configure_grid_options(domLayout="normal")
    gridOptions = grid.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        height=500,
        width="100%",
        theme="balham",
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        allow_unsafe_jscode=True,
    )

    return grid_response["selected_rows"]


def draw_world_map(tiles: str):
    """Create empty map centered on the coordinates (0,0) with given map tileset"""

    map = folium.Map(
        location=[30, 130],  # 調整到以台灣為相對合理的視角
        zoom_start=5,  # 初始縮放級別
        min_zoom=1.5,
        min_lon=-250,
        max_lon=250,
        min_lat=-85,
        max_lat=85,
        max_bounds=True,
        tiles=tiles,
        attr="Latest Earthquakes",
    )

    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position="bottomleft",
        separator=" | ",
        empty_string="NaN",
        lng_first=False,
        num_digits=20,
        prefix="Coordinates(lat | lon):",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(map)

    return map


def magnitude_colorcode(mag: float) -> str:

    if mag >= 7:
        return "red"
    elif 7 > mag >= 6:
        return "orange"
    elif 6 > mag >= 5:
        return "green"
    return "blue"


def add_map_marker(map, lat: float, lon: float, mag: float, depth: float, place: str):
    """Add marker and info popup to map"""

    marker_color = magnitude_colorcode(mag=mag)

    info = f"""<center> <b> {place} </b> </center>
    <br> <center> <b> Mag: {float(round(mag, 1))} </b> <center>
    <center> Depth: {depth} km  </center>
    <br> <center> Latitude/Longitude: {lat}/{lon} </center>
    """
    popup = folium.Popup(info)
    marker_location = (lat, lon)
    folium.Marker(
        location=marker_location,
        popup=popup,
        icon=folium.Icon(icon="info-sign", color=marker_color),
    ).add_to(map)


def map_layer_panel() -> str:
    """Create map layer panel and returns selected tiles from the panel"""

    layers = ["Base Map", "World Imagery", "Street Map"]
    map_layer = st.selectbox("Select map layer", layers)

    if map_layer == layers[0]:
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
    elif map_layer == layers[1]:
        tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    elif map_layer == layers[2]:
        tiles = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

    return tiles


def circle_search_panel(map, df: pd.DataFrame) -> tuple:
    """Creates search area input panel and returns latitude, longitude and radius values"""

    with st.form(key="Area Parameters", clear_on_submit=False):

        lat_input = st.number_input(
            label="Latitude",
            value=39.57,
            min_value=-90.0,
            max_value=90.0,
            format="%.15f",
        )
        lon_input = st.number_input(
            label="Longitude",
            value=32.53,
            min_value=-180.0,
            max_value=180.0,
            format="%.15f",
        )
        radius_input = st.slider(
            label="Radius (km)", min_value=0, max_value=1000, step=5
        )

        st.form_submit_button("Apply")

    return lat_input, lon_input, radius_input


def create_hourly_distribution_bar_chart(df: pd.DataFrame, x_axis: str, y_axis: str):
    """Creates hourly distribution bar chart with given x and y axis values"""

    events = df.loc[:, y_axis].tolist()
    scale = alt.Scale(domain=[0, max(events) + max(events) / 10])

    bars = (
        alt.Chart(data=df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(x_axis),
            y=alt.Y(y_axis, scale=scale),
            color=alt.condition(
                alt.datum[y_axis] == max(events),
                alt.value("orange"),
                alt.value("steelblue"),
            ),
        )
    )

    text = bars.mark_text(
        align="center", baseline="middle", dy=-10  # Moves text up
    ).encode(text=f"{y_axis}:O")

    st.altair_chart(bars + text, use_container_width=True)


def create_magnitude_bar_chart(df: pd.DataFrame, x_axis: str, y_axis: str):
    """Creates magnitude bar chart with given x and y axis values"""

    events = df.loc[:, y_axis].tolist()
    scale = alt.Scale(domain=[0, max(events) + max(events) / 10])

    bars = (
        alt.Chart(data=df)
        .mark_bar(cornerRadiusTopLeft=2, cornerRadiusTopRight=2)
        .encode(
            x=alt.X(x_axis),
            y=alt.Y(y_axis, scale=scale),
            color=alt.condition(
                alt.datum[y_axis] == max(events),
                alt.value("orange"),
                alt.value("steelblue"),
            ),
            tooltip=[x_axis, y_axis],
        )
        .interactive()
    )

    st.altair_chart(bars, use_container_width=True)


def create_worldwide_earthquakes_bar_chart(df: pd.DataFrame, x_axis: str, y_axis: str):
    """Creates annual earthquake bar chart with given x and y axis values"""

    events = df.loc[:, y_axis].tolist()
    scale = alt.Scale(domain=[0, max(events) + max(events) / 10])

    bars = (
        alt.Chart(data=df)
        .mark_bar(
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
        )
        .encode(
            x=alt.X(x_axis),
            y=alt.Y(y_axis, scale=scale),
            color=alt.condition(
                alt.datum[y_axis] == max(events),
                alt.value("orange"),
                alt.value("steelblue"),
            ),
        )
    )

    text = bars.mark_text(
        align="center", baseline="middle", dy=-10  # Moves text up
    ).encode(text=f"{y_axis}:O")

    rule = alt.Chart(df).mark_rule(color="red").encode(y=f"mean({y_axis}):Q")

    st.altair_chart(bars + rule + text, use_container_width=True)


def create_scattergeo_map(lat: list, lon: list, hovertext: list):
    """Creates 3d outline map with given latitude, longitude and popup text list"""
    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            name="",
            lat=lat,
            lon=lon,
            hovertext=hovertext,
            mode="markers",
            marker=dict(size=15, opacity=0.6, color="firebrick", symbol="circle"),
        )
    )

    fig.update_geos(projection_type="orthographic")
    fig.update_layout(width=750, height=750)

    st.plotly_chart(fig, use_container_width=True)
