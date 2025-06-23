# import libraries
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import timedelta, date

st.title("📈 Individual Stock Analysis")

# fetch data using yahoo finance API

@st.cache_data
def fetch_data(tickers: tuple, timeframe: tuple):
    data = yf.download(tickers, start = timeframe[0], end = timeframe[1])['Close'].sort_index()
    return data

# display data on streamlit interface

def display():
    try:
        with st.spinner("Downloading data..."):
            data = fetch_data(selected_tickers, selected_time)
        if data.empty:
            st.write("Invalid request. Check tickers or date range.")
        else:
            historic_data(data)
            display_price(data)
            daily_returns(data)
            calculate_metrics(data)
            return_spread(data)
    except:
        st.write("Must select one or more tickers to display.")

# fetches and formats historic data

def historic_data(data):
    st.header("Historic Price Trends")
    st.write("Head rows")
    st.dataframe(data.head())
    st.write("Tail rows")
    st.dataframe(data.tail())

# plots historic price trends 
def display_price(data):
    plot = sns.lineplot(data=data)
    plot.set(xlabel='Date', ylabel='Adjusted Closing Price')
    st.pyplot(plot.get_figure())
    plt.close()

# fetches and formats daily returns

def daily_returns(data):
    data_pct = data.pct_change().dropna()
    st.header("Daily Returns")
    st.write("Head rows")
    st.dataframe(data_pct.head().style.format("{:.2%}"))
    st.write("Tail rows")
    st.dataframe(data_pct.tail().style.format("{:.2%}"))
    st.header("Returns Data Overview")
    st.write(data_pct.describe())

# calculates metrics avg. daily return, daily volatility, annual volatility, total cum. return

def calculate_metrics(data):
    st.header("Returns Metrics")
    daily_return = data.pct_change().dropna()
    # avg. daily return
    avg_daily_return = daily_return.mean()
    # daily volatility
    daily_volatility = daily_return.std()
    # annual volatility
    annual_volatility = daily_volatility * np.sqrt(252)
    # total cum. return
    total_return = (daily_return+1).cumprod().iloc[-1]
    # join metrics
    metrics = pd.concat([avg_daily_return, daily_volatility, annual_volatility, total_return], axis='columns', ignore_index=True).set_axis(['Avg. Daily Return', 'Daily Volatility', 'Annual Volatility', 'Total Cum. Product'], axis='columns')

    # display as df
    # st.dataframe(metrics.style.format("{:.2%}"))

    # display as metrics
    for ticker in selected_tickers:
        st.write(ticker.upper())
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label=metrics.columns[0], value=f"{metrics.loc[ticker.upper()][0]:.3%}")
        col2.metric(label=metrics.columns[1], value=f"{metrics.loc[ticker.upper()][1]:.3%}")
        col3.metric(label=metrics.columns[2], value=f"{metrics.loc[ticker.upper()][2]:.3%}")
        col4.metric(label=metrics.columns[3], value=f"{metrics.loc[ticker.upper()][3]:.3%}")

# plot showing spread and pattern of returns 

def return_spread(data):
    st.header("Previous Volatility")
    plot = sns.histplot(data=data.pct_change().dropna(), element='step', stat='percent', kde=True, bins=30)
    plot.set(xlabel='Daily Return')
    st.pyplot(plot.get_figure())
    plt.close()

# check for submission

if "start" in st.session_state and st.session_state["start"]:
    selected_tickers = st.session_state["selected_tickers"]
    selected_time = st.session_state["selected_time"]
    display()
else:
    st.write("Select details on sidebar to view data.")
