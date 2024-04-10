
# Latest Earthquakes

#### Web App: [https://cs50p-eq.streamlit.app/](https://cs50p-eq.streamlit.app/)
#### Video Demo: [https://youtu.be/KzfQKydDKnI](https://youtu.be/KzfQKydDKnI)

This web app is made for CS50P Final Project using streamlit. It helps users to filter and
visualize latest earthquake data that provided by USGS (United States Geological Survey).

![screenshot](https://github.com/gorkemuna1/Latest-Earthquakes/blob/main/images/main.png?raw=true)
## Table of Contents

* [Built With](#built-with)
* [Data Sources](#data-sources)
    * [Variables Reference](#variables-reference)
* [Usage](#usage)
    * [Filters](#filters)
    * [Dataframe](#dataframe)
    * [Map Markers](#map-markers)
    * [Map Panels](#map-panels)
    * [Outline Map and Graphs](#map-panels)
* [Installation](#installation)
* [Authors](#authors)

## Built With

* [Streamlit](https://streamlit.io/): Streamlit turns python scripts into shareable web apps without any front‑end experience.
* [Folium](https://python-visualization.github.io/folium/): Python library that allows you to create interactive maps using the Leaflet.js library.
* [Altair](https://altair-viz.github.io/): Python library for creating interactive visualizations.
* [Plotly](https://plotly.com/python/): Python library for creating interactive visualizations using D3.js visualization library.
* [ag-Grid](https://pypi.org/project/streamlit-aggrid/): Library for creating data grids and displaying tabular data.
* [pandas](https://pandas.pydata.org/docs/): Python library for data manipulation and analysis.
* [haversine](https://pypi.org/project/haversine/): Python library that provides a function for calculating the Haversine distance between two coordinates.

* [Filter UI idea](https://discuss.streamlit.io/t/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter-dataframe/29470): Non-automated version is used with additional features. Thanks to Tyler Richards, Arnaud Miribel and Zachary Blackwood for providing this streamlit filter UI. 

## Data Sources

**This is not a real-time feed** and app uses monthly csv dataset provided by [USGS](https://earthquake.usgs.gov/) in the background. 
* Streamlit feature `@st.experimental_memo` is used while accessing this csv file.
* [@st.experimental_memo](https://docs.streamlit.io/library/api-reference/performance/st.experimental_memo) is the **function decorator** to memoize function executions.
* **Memoization** is really useful for improving the performance of Streamlit app by avoiding the need to recalculate the output of a function or component each time it is called.
* Since Streamlit will be re-running the entire script after each interaction, this step is necessary to improve performance.

### Variables Reference

|time (UTC)                 |latitude  |longitude   |depth   |mag |magType|place                          |type       |status    |locationSource|magSource|
|---------------------------|----------|------------|--------|----|-------|-------------------------------|-----------|----------|--------------|---------|
|2022-12-26T17:28:01.550000 |19.387500 |-155.282836 |1.02    |2.1 |md     |"7 km SW of Volcano, Hawaii"   |earthquake |automatic |hv            |hv       |
|2022-12-26T14:30:07.119000 |-17.622   |-69.713     |167.538 |4.4 |mb     |"Peru-Bolivia border region"   |earthquake |reviewed  |us            |us       |
|2022-12-26T09:35:02.485000 |-58.6443  |-25.0232    |19.159  |5.1 |mww    |"South Sandwich Islands region"|earthquake |reviewed  |us            |us       |

## Usage

### Filters

* You can change your dataset size before applying any additional filters. It will show **past 30 days** by default.
* Selecting **add more filters** option will show you more filtering options. You can select in any order and change or remove them whenever you want.
* All filter changes will apply to both interactive and 3d-outline maps and given earthquake related graphs.

![screenshot](https://github.com/gorkemuna1/Latest-Earthquakes/blob/main/images/filters.png?raw=true)

### Dataframe

* Dataframe will be displayed with python version of ag-Grid JavaScript library.
* All filter changes will apply to dataframe aswell and it will also display color-coded magnitude values.
* You can select any **magnitude 4.0+** earthquake row with checkbox right next to it and display it as a marker in interactive map.
* Checkbox in the top left corner can be used to select all rows. (This will automatically ignore earthquakes below 4.0 magnitude if there are no additional filters applied.)
* You can sort columns by clicking column names or adjust column width. There is also built-in ag-Grid filter with less options.

![screenshot](https://github.com/gorkemuna1/Latest-Earthquakes/blob/main/images/dataframe.png?raw=true)

### Map Markers

* You can select a row from the dataframe by checking the checkbox next to it.
* Selected row will be shown on the map as a marker if magnitude value is equal to 4.0 or higher.
* Magnitude value is limited to avoid longer loading times.
* Markers are color-coded depending on magnitude value.
* You can click any marker and check details.

![screenshot](https://github.com/gorkemuna1/Latest-Earthquakes/blob/main/images/markers.png?raw=true)

### Map Panels

* You can choose map layer. Base Map layer gives the best performance.
* Heatmap and Circle Search panels are affected by the data filter.
* Heatmap works with filtered dataframe so you don't have to select rows to display them.
* Selecting Heatmap option will disable markers and circle search panel.
* You can scroll over and add/remove filters while performing a circle search.
* You can check distance in between center location and nearest/furthest earthquakes while performing a circle search.

![screenshot](https://github.com/gorkemuna1/Latest-Earthquakes/blob/main/images/circle-search.png?raw=true)

### Outline Map and Graphs

* 3d-outline map is added for visual reference while checking given earthquake graphs.

![screenshot](https://github.com/gorkemuna1/Latest-Earthquakes/blob/main/images/graphs.png?raw=true)

## Installation

### Local Setup
1. Clone the repository
2. Create a virtual environment (optional)
```sh
virtualenv venv
source venv/bin/activate
```
3. Install required libraries
```sh
python -m pip install -r requirements.txt
```
4. Run the Streamlit web app
```sh
streamlit run project.py
```

## Authors
[Görkem Ünal](https://github.com/gorkemuna1)
