import altair as alt
import pandas as pd
import streamlit as st

from common.constants import GithubTrendingDateRange
from common.handlers import GithubTrendingHandler


@st.cache_data(ttl=5 * 60)
def get_github_trending_chart(
    date_range: GithubTrendingDateRange
) -> alt.Chart:
    df_repos: pd.DataFrame = pd.DataFrame(
        GithubTrendingHandler(date_range=date_range).get_json_repos_data(),
    )
    df_repos = df_repos.rename(
        columns={
            "full_name": "Repository name",
            "stars_count": "Stars count",
            "trending_stars_count": "Trending stars count",
        }
    )

    trending_chart_data: alt.Chart = (
        alt.Chart(df_repos)
        .mark_bar()
        .encode(
            x=alt.X("Repository name", sort=None),
            y=alt.Y("Trending stars count", sort=None),
            tooltip=["Repository name", "Trending stars count", "Stars count"],
        )
        .interactive()
    )
    return trending_chart_data


# Draw charts
st.title("Github Trending Python Repositories")
tab1, tab2, tab3 = st.tabs(["Today", "This week", "This month"])
with tab1:
    st.altair_chart(
        get_github_trending_chart(date_range=GithubTrendingDateRange.daily),
        use_container_width=True,
    )
with tab2:
    st.altair_chart(
        get_github_trending_chart(date_range=GithubTrendingDateRange.weekly),
        use_container_width=True,
    )
with tab3:
    st.altair_chart(
        get_github_trending_chart(date_range=GithubTrendingDateRange.monthly),
        use_container_width=True,
    )
