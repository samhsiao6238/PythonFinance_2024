import streamlit as st
import pandas as pd
# 引入folium庫，用於建立地圖
import folium
# 從geopy庫引入Nominatim，用於地理編碼和反編碼（地址<->座標）
from geopy.geocoders import Nominatim
# 引入 st_folium 可在 Streamlit 應用中嵌入 Folium 地圖
from streamlit_folium import st_folium
# 引入 st_lottie 以在 Streamlit 應用中嵌入 Lottie 動畫
from streamlit_lottie import st_lottie
# 引入 haversine 用於計算兩個地理座標之間的距離
from haversine import haversine
# 引入 requests 用於執行 HTTP 請求
import requests
# 引入自訂庫
import utility
# 引入 HeatMap、PolyLineTextPath 用於在地圖上添加熱力圖和帶文字的多邊形路徑
from folium.plugins import HeatMap, PolyLineTextPath


def main():
    # 近期地震等級 2 以上的地震
    st.title(body="近期地震等級 2 以上的地震")
    # 從 USGS 取得地震數據 csv
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv"
    # 自訂的函數 get_dataframe
    df = get_dataframe(url)
    # 建立一個副本，用於操作數據但不影響原資料
    # 使用 sidebar 插件建立側邊欄位
    sidebar_df = df.copy()

    # 建立 sidebar
    with st.sidebar:
        # 建立 Sidebar 動畫
        lottie_url = "https://assets7.lottiefiles.com/packages/lf20_kc6thomq.json"
        # 調用自訂函數取回資料
        lottie_json = utility.load_lottieurl(lottie_url)
        st_lottie(
            lottie_json,
            speed=1,
            height=200,
            key="initial",
            quality="low"
        )

        # 關於資料集的資訊 (地震等級 2 或以上)
        # 參數 unsafe_allow_html=True 允許在 Markdown 中使用 HTML 程式碼
        st.markdown(
            "<h3 style='text-align: center; color: firebrick;'>"
            "Quakes magnitude 2 or higher</h3>",
            unsafe_allow_html=True,
        )
        # 使用 st.columns() 建立兩個欄位（縱向）
        sidebar_col0, sidebar_col1 = st.columns(2)
        # 欄位一
        with sidebar_col0:
            st.info("Last 24 hours")
            st.info("Last 7 days")
            st.info("Last 30 days")

        # 欄位二
        with sidebar_col1:
            st.error(f"{len(utility.set_dataset_size(sidebar_df, 1))} Quakes")
            st.error(f"{len(utility.set_dataset_size(sidebar_df, 7))} Quakes")
            st.error(f"{len(utility.set_dataset_size(sidebar_df, 30))} Quakes")

        # 使用展開視窗建立「關於」
        with st.expander("About"):
            st.markdown(
                """
                This web app is made for **CS50's Introduction to Programming with Python Final Project**.
                It helps users to filter and visualize latest earthquake data that provided by
                **USGS** (United States Geological Survey).
                """
            )

    # 調用自訂的函數篩選數據
    df = utility.data_filter(df)

    # Creating ag-Grid table
    selected = utility.create_data_grid(df)

    # Adjusting position of refresh and download buttons
    button_col1, button_col2, button_col3 = st.columns((1.2, 2, 8))

    # Refresh button
    with button_col1:
        refresh_button = st.button(
            label="Refresh Dataset",
            help="Resets dataset cache and reruns the entire page",
        )
        if refresh_button:
            st.experimental_memo.clear()
            st.experimental_rerun()

    # Convert current dataframe to csv and add download button for it
    with button_col2:
        csv = utility.convert_to_csv(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name="filtered_latest_eartquakes.csv",
            mime="text/csv",
        )

    st.text("")

    # TABS for map, graphs and stats
    tab1, tab2, tab3 = st.tabs(
        [
            "INTERACTIVE EARTHQUAKE MAP",
            "3D OUTLINE EARTHQUAKE MAP AND GRAPHS",
            "ANNUAL EARTHQUAKE STATISTICS",
        ]
    )

    with tab1:
        st.markdown(
            """ 
            * Selected row will be shown on the map as a marker if magnitude value is equal to 4.0 or higher.
            * Magnitude value is limited to avoid longer loading times.
            """
        )
        # map_col1 displays the map, map_col2 displays all the other widgets related to the map
        map_col1, map_col2 = st.columns((5, 1.26))

        # Starting with map_col2 because widget changes will be displayed on the map
        with map_col2:

            tiles = utility.map_layer_panel()
            map = utility.draw_world_map(tiles)
            # Heatmap
            if st.checkbox(
                "Show Heatmap", help="Dataframe filter changes will change results."
            ):

                HeatMap(
                    data=list(
                        zip(df.latitude.values, df.longitude.values, df.mag.values)
                    ),
                    radius=20,
                    min_opacity=0.6,
                    blur=15,
                ).add_to(map)
            # Circle Search
            elif st.checkbox(
                "Perform a circle search",
                help="Dataframe filter changes will change results.",
            ):

                lat, lon, radius = utility.circle_search_panel(map, df)

                st.session_state.location = find_location_by_coordinates(lat, lon)
                # Remove # below to display location information under the circle search panel
                # st.info(f'Center Location: {st.session_state.location}')

                earthquakes_in_radius = []

                # Iterating over rows to check if they are in given radius
                for index, row in df.iterrows():
                    # Calculate the distance between two points on Earth using their latitude and longitude
                    # Distance in kilometers
                    distance = haversine(
                        (lat, lon), (row["latitude"], row["longitude"])
                    )

                    if distance <= radius:
                        utility.add_map_marker(
                            map,
                            lat=row["latitude"],
                            lon=row["longitude"],
                            mag=row["mag"],
                            depth=row["depth"],
                            place=row["place"],
                        )

                        earthquakes_in_radius.append(
                            (distance, row["latitude"], row["longitude"])
                        )

                # Adding circle area to the map
                circle_tooltip = f"""<center> <b>{len(earthquakes_in_radius)} earthquakes </b> found in <b> {radius} km </b> radius </center>"""

                folium.Circle(
                    location=[lat, lon],
                    radius=radius * 1000,  # Radius of the circle, in meters by default
                    fill=True,
                    color="firebrick",
                    tooltip=circle_tooltip,
                ).add_to(map)
                # Marking center of circle area
                folium.Marker(
                    location=[lat, lon],
                    popup=f"""<center> <b> Center Location </b> </center> <br> {st.session_state.location}""",
                    icon=folium.Icon(color="red", icon="arrow-down"),
                ).add_to(map)

                if st.checkbox("Show nearest earthquake"):
                    try:
                        min_distance = min(
                            earthquake[0] for earthquake in earthquakes_in_radius
                        )
                    except ValueError:
                        pass

                    for earthquake in earthquakes_in_radius:
                        if earthquake[0] == min_distance:  # comparing distances
                            line = folium.PolyLine(
                                [(lat, lon), (earthquake[1], earthquake[2])],
                                color="firebrick",
                                weight=5,
                                opacity=1,
                            ).add_to(map)

                            attr = {
                                "fill": "firebrick",
                                "font-weight": "bold",
                                "font-size": "15",
                            }

                            PolyLineTextPath(
                                line,
                                text=f"Nearest ⮞ {round(earthquake[0])} km",
                                center=True,
                                offset=15,
                                attributes=attr,
                            ).add_to(map)
                # Nearest and Furthest eartquakes
                if (
                    st.checkbox("Show furthest earthquake")
                    and len(earthquakes_in_radius) > 1
                ):
                    try:
                        max_distance = max(
                            earthquake[0] for earthquake in earthquakes_in_radius
                        )
                    except ValueError:
                        pass

                    for earthquake in earthquakes_in_radius:
                        if earthquake[0] == max_distance:
                            line = folium.PolyLine(
                                [(lat, lon), (earthquake[1], earthquake[2])],
                                color="royalblue",
                                weight=5,
                                opacity=1,
                            ).add_to(map)

                            attr = {
                                "fill": "royalblue",
                                "font-weight": "bold",
                                "font-size": "15",
                            }

                            PolyLineTextPath(
                                line,
                                f"Furthest ⮞ {round(earthquake[0])} km",
                                center=True,
                                offset=15,
                                attributes=attr,
                            ).add_to(map)
            # Showing selected markers if other two options(heatmap and circle search) are not active
            elif len(selected) > 0:

                for i in range(len(selected)):
                    if selected[i]["mag"] >= 4:
                        utility.add_map_marker(
                            map,
                            lat=selected[i]["latitude"],
                            lon=selected[i]["longitude"],
                            mag=selected[i]["mag"],
                            depth=selected[i]["depth"],
                            place=selected[i]["place"],
                        )

        with map_col1:
            # Updating the map on streamlit
            st_folium(map, width=1145, height=640)

    with tab2:

        tab2_col1, tab2_col2 = st.columns(2)
        with tab2_col1:
            st.write("")
            # 3D Outline map
            utility.create_scattergeo_map(
                lat=df["latitude"].tolist(),
                lon=df["longitude"].tolist(),
                hovertext=df["place"].tolist(),
            )

        with tab2_col2:
            st.write("")
            st.markdown(
                "<h6 style='text-align: center; color: firebrick;'>Hourly distribution of the number of earthquakes (Magnitude 2 or higher)</h6>",
                unsafe_allow_html=True,
            )

            if len(df) > 0:
                hours_str = ["%.2d" % i for i in range(24)]
                x_axis_label = [x + ":00 - " + x + ":59" for x in hours_str]
                # Creating a list of the number of earthquakes that occured in each hour
                hourly_eartquake_count = [
                    len(
                        df.loc[
                            df["time (UTC)"].astype("datetime64").dt.hour == hour
                        ].index
                    )
                    for hour in range(24)
                ]

                chart_data1 = pd.DataFrame(
                    {
                        "Time Period": x_axis_label,
                        "Number of Events": hourly_eartquake_count,
                    }
                )

                utility.create_hourly_distribution_bar_chart(
                    df=chart_data1, x_axis="Time Period", y_axis="Number of Events"
                )

            else:
                st.warning("There are no values to show")

            st.markdown(
                "<h6 style='text-align: center; color: firebrick;'>Histogram of all the earthquakes in terms of magnitude (Magnitude 2 or higher)</h6>",
                unsafe_allow_html=True,
            )

            if len(df) > 0:
                magnitudes = sorted(df["mag"].unique())
                # Creating a list of the number of events for each magnitude value
                events = [len(df.loc[df["mag"] == mag]) for mag in magnitudes]

                chart_data2 = pd.DataFrame(
                    {"Magnitude": magnitudes, "Number of Events": events}
                )

                utility.create_magnitude_bar_chart(
                    df=chart_data2, x_axis="Magnitude", y_axis="Number of Events"
                )
            else:
                st.warning("There are no values to show")

    with tab3:
        tab3_col1, tab3_col2, tab3_col3 = st.columns((1, 2, 1))

        with tab3_col2:

            st.markdown(
                "<h5 style='text-align: center; color: firebrick;'>Number of Earthquakes per Year</h5>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h6 style='text-align: center; color: firebrick;'>Magnitude 5 or higher</h6>",
                unsafe_allow_html=True,
            )

            year = st.selectbox(
                label="Choose time period",
                options=["2000-2021", "1990-1999"],
            )

            magnitude = st.radio(
                label="Choose magnitude range",
                options=["All", "5–5.9", "6–6.9", "7–7.9", "8.0+"],
                horizontal=True,
            )

            url = "https://www.usgs.gov/programs/earthquake-hazards/lists-maps-and-statistics"
            df_list = get_worldwide_earthquakes_chart_data(url)

            # 有五個資料表，分別是「全球（2000–2021）、美國地震（2000-2012）、全球（1990-1999）
            # 美國（1990-1999）、美國各州（2010-2015）M3+」
            # 要使用全球的數據，所以判斷索引（0、2）的年份，（2000-2012）是（0）
            # 刪除索引為[4]的row，特別注意，這裡並不關注起始索引值，而是直接判斷[4]這個索引
            raw_data = df_list[0 if year == "2000-2021" else 2].drop(4)
            raw_data = raw_data.set_index("Magnitude")
            raw_data = raw_data.astype(int)
            raw_data.loc["All"] = raw_data.sum(axis=0)

            # Using transpose of the array as chart data
            chart_data = raw_data.T
            chart_data.rename(
                columns={chart_data.columns[0]: "8.0+"}, inplace=True, errors="raise"
            )
            chart_data = pd.DataFrame(
                {
                    "Years": chart_data.index,
                    "Number of Events": chart_data[magnitude].tolist(),
                }
            )

            utility.create_worldwide_earthquakes_bar_chart(
                df=chart_data, x_axis="Years", y_axis="Number of Events"
            )

            with st.expander("Show raw data and source for this graph"):
                st.dataframe(raw_data)

                csv = utility.convert_to_csv(raw_data)
                st.download_button(
                    label="Download raw data as CSV",
                    data=csv,
                    file_name=f"earthquakes_{year}.csv",
                    mime="text/csv",
                )
                # Given data source
                st.write(
                    "**Data Source:** [usgs.gov](https://www.usgs.gov/programs/earthquake-hazards/lists-maps-and-statistics)"
                )


# @st.experimental_memo 是 Streamlit 的一個裝飾器，用於快取函數的結果。
# 當函數在相同的輸入參數下被多次調用時，Streamlit 不會重新計算函數，而是直接傳回先前快取的結果。
# 可以顯著提高應用的效能，尤其是在處理耗時的資料載入、處理或計算時。
@st.experimental_memo
def get_dataframe(url: str) -> pd.DataFrame:
    """從給定的 url 讀取 csv 檔案，並在處理後返回 dataframe"""
    # 指定欄位
    filters = [
        "time",
        "latitude",
        "longitude",
        "depth",
        "mag",
        "magType",
        "place",
        "type",
        "locationSource",
        "magSource",
        "status",
    ]
    # 讀取傳入的 csv 檔案，並透過參數「usecols」指定需要的資料欄位
    df = pd.read_csv(url, usecols=filters)
    # 「dropna」移除缺失值（NaN）的欄位
    # 「reset_index」並重置索引（從 0 開始）
    # 「drop=True」不要保留原來的索引
    df = df.dropna().reset_index(drop=True)
    # 忽略資料中地震強度低於 2 的數據
    df = df.loc[df["mag"] >= 2]
    # 強度四捨五入到小數點第一位
    df["mag"] = df["mag"].round(1)
    # 深度四捨五入到小數點第四位
    df["depth"] = df["depth"].round(4)
    # 將「time」更名為「time (UTC)」
    # 「inplace=True」表示會對原始數據進行更改
    # 「errors="raise"」表示如果出現錯誤，就會拋出異常，相反的參數值是「ignore」
    df.rename(columns={"time": "time (UTC)"}, inplace=True, errors="raise")
    # 取得全部索引後，對其映射到從「0」開始的數組
    df.index = df.index.factorize()[0]
    return df


@st.experimental_memo
def get_worldwide_earthquakes_chart_data(url: str) -> list[pd.DataFrame]:
    """Returns list of dataframes from given url"""

    html = requests.get(url).content
    df_list = pd.read_html(html)

    return df_list


def find_location_by_coordinates(lat: float, lon: float):
    """Returns location information of given latitude and longitude using Nomatim API."""

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((f"{lat},{lon}"), language="en")
    if location is None:
        location = "Unknown"

    return location


if __name__ == "__main__":

    PROJECT_TITLE = "Latest Earthquakes"
    st.set_page_config(
        page_title=PROJECT_TITLE,
        initial_sidebar_state="expanded",
        layout="wide",
    )

    # Changing expander background color
    st.markdown(
        """
    <style>
    .streamlit-expanderHeader {
    #   font-weight: bold;
        background: #E8DFDF;
        font-size: 15px;
    }
    .streamlit-expanderContent {
    #   font-weight: bold;
        background: #E8DFDF;
        font-size: 15px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Initiating session state for location information
    if "location" not in st.session_state:
        st.session_state.location = None

    main()
