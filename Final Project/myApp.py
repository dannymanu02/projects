import os

from utils.b2 import B2
from dotenv import load_dotenv

import streamlit as st

import pandas as pd
import plotly.graph_objects as go

load_dotenv()

st.set_page_config(layout="wide")

def page_style():
    gradient = """
    <style>
    [data-testid="stAppViewBlockContainer"]{
    # background-color: #D9AFD9;
    # background-image: linear-gradient(-235deg, #D9AFD9 0%, #97D9E1 100%);
    # background-image: linear-gradient( 95.2deg, rgba(173,252,234,1) 26.8%, rgba(192,229,246,1) 64% );
    background-image: linear-gradient(to right, #ffefba, #ffffff);
    }
    </style>
    """
    st.markdown(gradient, unsafe_allow_html=True)
    st.markdown("<Center><H1> r/WorldNews Analysis</H1></Center>", unsafe_allow_html = True)

@st.cache_data
def get_data(file_name):
    # collect data frame of reviews and their sentiment
    b2.set_bucket(os.environ['B2_BUCKETNAME'])
    df_reddit = b2.get_df(file_name)

    
    return df_reddit
# st.image("reddit_logo.png", width=200)
page_style()

b2 = B2(endpoint=os.environ['B2_ENDPOINT'],
        key_id=os.environ['B2_keyID'],
        secret_key=os.environ['B2_applicationKey'])

df_reddit = get_data("reddit_worldnews_sentiments_clean.csv")
df_analysis = get_data("cumilative_headlines.csv")

st.markdown("<H3>Analysis of behavior of reddit users on the r/worldnews subreddit<H3>", unsafe_allow_html=True)

html_string = """<ul> <li>For this assignment I will analyse the posts in top section, 
I wan to see what kind of sentiment gets more upvotes, 
is it the negative news or the positive ones or the neutral ones, let's see!</li></ul>"""

st.markdown(html_string, unsafe_allow_html=True)

top_articles = df_reddit[df_reddit['Post_Category'] == 'Top']

top_articles_grouped = top_articles.groupby("Sentiment_Label").agg("Upvotes").sum().reset_index()
top_articles_grouped.columns = ["Sentiment_Label", "Upvotes"]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=top_articles_grouped["Sentiment_Label"],
    y=top_articles_grouped["Upvotes"],
    marker=dict(color=['#FF6347', '#87CEEB', '#32CD32']),  # Colors for negative, neutral, and positive sentiments
    hovertemplate='<b>%{x}</b><br>Count: %{y}',  # Hover template
))

# Update layout
fig.update_layout(
    title='Sentiment Distribution of Top Articles',
    xaxis=dict(title='Sentiment'),
    yaxis=dict(title='Count'),
    font=dict(family='Arial', size=12),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
    hovermode='x',
)

st.plotly_chart(fig)

st.write("From the above graph it is clear that people on the internet like negative news, news that is controversial and dividing.")
st.markdown("<b>The Plot was derived from the below data: </b>", unsafe_allow_html=True)
st.dataframe(df_reddit.head(25))


