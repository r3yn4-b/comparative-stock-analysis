# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from utils import fetch_data, colors
st.title("📈 Individual Stock Analysis")

# display data on streamlit interface

def display():
    try:
        with st.spinner("Downloading data..."):
            data = fetch_data(selected_tickers, selected_time)
            pct_data = data.pct_change().dropna()
        if data.empty:
            st.write("Invalid request. Check tickers or date range.")
        else:
            display_price(data)
            historic_data(data)
            calculate_metrics(pct_data)
            daily_returns(pct_data)
            return_spread(pct_data)
    except:
        st.header("Must select one or more tickers to display.")

# fetches and formats historic data

def historic_data(data):
    col1, col2 = st.columns(2)
    col1.subheader("Head rows")
    col1.dataframe(data.head().style.format('${:.2f}'))
    col2.subheader("Tail rows")
    col2.dataframe(data.tail().style.format('${:.2f}'))
    st.write("Head and tail data has been displayed to observe general movement over the selected timeframe.")

# plots historic price trends 
def display_price(data):
    st.header("Historic Price Trends")
    st.write("Below is the historical data of each asset's performance over the selected timeframe. Adjusted Closing Price is given in USD.")
    plot = sns.lineplot(data=data, linewidth=1)
    plot.set(xlabel='Date', ylabel='Adjusted Closing Price')
    st.pyplot(plot.get_figure())
    plt.close()

# fetches and formats daily returns

def daily_returns(pct_data):
    # tabulated overview
    col1, col2 = st.columns(2)
    col1.subheader("Head rows")
    col1.dataframe(pct_data.head().style.map(colors).format("{:.2%}"))
    col2.subheader("Tail rows")
    col2.dataframe(pct_data.tail().style.map(colors).format("{:.2%}"))
    st.write("Head and tail data has been displayed to observe general movement over the selected timeframe.")

# calculates metrics avg. daily return, daily volatility, annual volatility, total cum. return

def calculate_metrics(pct_data):
    st.header("Daily Returns Data Overview")
    st.write("Individual metrics for each asset's percentage returns over the selected timeframe are shown below.")
    daily_return = pct_data
    # avg. daily return
    avg_daily_return = daily_return.mean()
    # daily volatility
    daily_volatility = daily_return.std()
    # annual volatility
    annual_volatility = daily_volatility * np.sqrt(252)
    # total cum. return
    total_return = (daily_return+1).cumprod().iloc[-1] - 1
    # join metrics
    metrics = pd.concat([avg_daily_return, daily_volatility, annual_volatility, total_return], axis='columns', ignore_index=True).set_axis(['Avg. Daily Return', 'Daily Volatility', 'Annual Volatility', 'Total Cum. Return'], axis='columns')

    # display as df
    # st.dataframe(metrics.style.format("{:.2%}"))

    # display as metrics
    for ticker in selected_tickers:
        st.subheader(ticker.upper())
        columns = st.columns(4)
        for i in range(0, 4):
            with columns[i]:
                item = f"{metrics.loc[ticker.upper()].iloc[i]:.3%}"
                st.metric(label=metrics.columns[i], value=item)
                st.divider()


# plot showing spread and pattern of returns 

def return_spread(pct_data):
    st.header("Historical Daily Returns Volatility")
    st.write("The deviation of returns from its mean has been plotted to show the volatility of each asset's performance. Data spread farther from its peak, and with a lower peak, are more volatile as daily returns span over a greater range.")
    plot = sns.histplot(data=pct_data*100, element='step', stat='density', kde=True, bins=30)
    plot.set(xlabel='Daily Return (%)')
    st.pyplot(plot.get_figure())
    plt.close()
    st.write("A left-biased peak shows that returns have historically been more concentrated below the mean than above it, and vice versa for a right-biased peak. This can give some insight into what future trends may follow.")

# check for submission and run page

st.write("This page analyses each input asset and provides individual data. To view overall portfolio performance, select the 'Portfolio Analysis' tab.")

if "start" in st.session_state and st.session_state["start"]:
    selected_tickers = st.session_state["selected_tickers"]
    selected_time = st.session_state["selected_time"]
    display()
else:
    st.subheader("Select details on sidebar to view data.")
