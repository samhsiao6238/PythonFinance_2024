import streamlit as st

st.set_page_config(page_title="Home immo data vise", page_icon="🏠")

st.write("# Welcome to my Streamlit for my data vise! 👋")
st.write("# Welcome to my Streamlit for my data vise! 👋")

st.sidebar.success("Select your data vise.")

article_url = "https://medium.com/p/09d9a643a27f"
st.markdown(
    f"""
    My Streamlit project is a case study to explore data collected through web scraping. Streamlit is an open-source app framework specifically built for Machine Learning and Data Science projects. **👈 Select a demo from the sidebar** to see examples of what Streamlit can achieve!

    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Dive into our [documentation](https://docs.streamlit.io)
    - Ask questions in our [community forums](https://discuss.streamlit.io)

    ### Explore more complex demos
    - Use a neural network to [analyze the Udacity Self-driving Car Image Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)

    To learn more about the scraper used in this project, check out [my latest article]({article_url}).
    """
)