# import libraries
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import timedelta, date

# fetch data function

@st.cache_data
def fetch_data(tickers: tuple, timeframe: tuple):
    data = yf.download(tickers, start = timeframe[0], end = timeframe[1])['Close'].sort_index()
    return data

def display():
    try:
        st.header("Adjusted Close")
        data = fetch_data(selected_tickers, selected_time).head()
        st.dataframe(pd.concat([data.head(), data.tail()]))
    except:
        st.write("Must select one or more tickers to display.")

# streamlit page

#setup
st.set_page_config(page_title="Comparative Stock Analysis and Basic Portfolio Metrics", page_icon=":bar_chart:", initial_sidebar_state="auto")
st.title("Comparative Stock Analysis and Basic Portfolio Metrics")
# add ticker select as a dropdown
default_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM", "KO", "XOM", "TSLA", "PG", "NVDA", "V", "UNH", "LLY"]
selected_tickers = st.sidebar.multiselect('Ticker Select', default_options, accept_new_options=True, max_selections=5)
# start date and end date
end = date.today()
start = (end - pd.DateOffset(years = 5)).date()
selected_time = st.sidebar.slider('Timeframe', value= (start, end))
submit = st.sidebar.button("Display Data")
# check for submission
if submit:
    display()




