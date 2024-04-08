"""
作者資訊：
Author - Gaurav Kabra
Dashboard in Streamlit and Plotly
Github：
https://github.com/kabragaurav/Dashboard-in-Streamlit
說明：
這個專案呈現美國航空公司推特的情緒分析
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# 取消警告
st.set_option("deprecation.showPyplotGlobalUse", False)

# 中央區域標題
st.title("Sentiment Analysis of Tweets on American ✈️")
# 中央區域標題描述
st.markdown(
    "Download data from [_Kaggle_] "
    "(https://www.kaggle.com/crowdflower/twitter-airline-sentiment). "
    "Note that maps won't work with this data though."
)

# 側邊欄位
st.sidebar.markdown("### 👨‍💻 *Gaurav Kabra*")
# 側邊欄位標題
st.sidebar.title("Options")


# 自訂函數：加載數據
# Caching data once loaded using decorator
# Makes sense since this data not updated in file
# May clear cache in top-right corner
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv("Tweets.csv")
    # standard datetime or dt
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data


# 調用加載數據的函數
data = load_data()

# 假如想查看資料內容
# st.write(data)

st.sidebar.subheader("Sample random tweet")
sample_tweet = st.sidebar.radio("Sentiment", ("positive", "negative", "neutral"))
# n is no. of tweets to query
# iat ensures data is extracted not series or dataframe
st.sidebar.markdown(
    data.query("airline_sentiment == @sample_tweet")[["text"]].sample(n=1).iat[0, 0]
)


st.sidebar.markdown("### Count of Tweets by Sentiment")
# key is like id. It ensures non-conflict if more than one selectboxes are present
plot_type = st.sidebar.selectbox("Type", ["Histogram", "Pie-chart"], key="rollno1")
sentiment_count = data["airline_sentiment"].value_counts()
sentiment_count = pd.DataFrame(
    {"Sentiment": sentiment_count.index, "Tweets": sentiment_count.values}
)

if st.sidebar.checkbox("Show", False, key="rollno2"):
    st.markdown("### Count of Tweets by Sentiment")
    if plot_type == "Histogram":
        fig = px.bar(
            sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=550
        )
        st.plotly_chart(fig)
    else:
        # else pie-chart
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
        st.plotly_chart(fig)


st.sidebar.subheader("Time & Location of Tweets")
hour = st.sidebar.slider("Hour of Day", 0, 23)
# hour = st.sidebar.number_input("Hour of Day", min_value=1, max_value=24)
# st.map(data)

modified_data = data[data["tweet_created"].dt.hour == hour]
if st.sidebar.checkbox("Show", True, key="rollno3"):
    st.markdown("### Locations of tweets on hour-basis")
    st.markdown(
        "{0} tweets between {1}:00 and {2}:00".format(
            len(modified_data), hour, (hour + 1) % 24
        )
    )
    st.map(modified_data)
    if st.sidebar.checkbox("View Details", False):
        st.write(modified_data)

st.sidebar.subheader("Compare Airlines")
airln = st.sidebar.multiselect(
    "Select Airline(s)",
    ("United", "American", "Southwest", "US Airways", "Virgin America", "Delta"),
    key="rollno4",
)

if len(airln) > 0:
    modified_data = data[data.airline.isin(airln)]
    fig = px.histogram(
        modified_data,
        "airline",
        y="airline_sentiment",
        histfunc="count",
        color="airline_sentiment",
        facet_col="airline_sentiment",
        labels={"airline_sentiment": "tweets"},
        height=550,
        width=550,
    )
    st.plotly_chart(fig)


# wordcloud : bigger the word in picture, stronger the word is
st.sidebar.header("WordCloud")
word_sentiment = st.sidebar.radio(
    "Select Sentiment", ("positive", "negative", "neutral")
)

if st.sidebar.checkbox("Show", True, key="rollno5"):
    st.header("WordCloud for {0} Sentiment".format(word_sentiment))
    df = data[data["airline_sentiment"] == word_sentiment]
    words = " ".join(df["text"])
    # words may be in links or mentions; RT=retweet
    pre_process = " ".join(
        [
            word
            for word in words.split()
            if "http" not in word and not word.startswith("@") and word != "RT"
        ]
    )
    # for stopwords refer nltk. Concisely they remove non-sense words like 'the'
    wc = WordCloud(
        stopwords=STOPWORDS, background_color="#000", height=550, width=550
    ).generate(pre_process)
    plt.imshow(wc)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
