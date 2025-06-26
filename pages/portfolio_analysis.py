# import libraries
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pages.individual_analysis import fetch_data, colors

st.title("📈 Portfolio Analysis")

# display data

def display():
    try:
        with st.spinner("Downloading data..."):
            data = fetch_data(selected_tickers, selected_time)
            pct_data = data.pct_change().dropna()
        if data.empty:
            st.write("Invalid request. Check tickers or date range.")
        elif len(data.columns) < 2:
            st.write("To display portfolio metrics, at least two tickers must be selected.")
        else:
            unweighted_returns(pct_data)
            get_weights(pct_data)
            correlation(pct_data)
    except:
        st.subheader("Must select one or more tickers to display.")

# calculate and display correlation between portfolio items

def correlation(pct_data):
    st.header('Asset Correlation')
    st.write("The correlation coefficient shown describles the movement of the stated assets with one another. A coefficient of +1 describes a perfect positive correlation while a correlation of -1 describles a perfect negative correlation.")
    correlation_data = pct_data.corr(method='pearson')
    columns = st.columns(3)

    # displays metrics of correlation coefficients
    # loops through only combinations of tickers that have not been shown before
    for x in range(0, len(selected_tickers)):
        for y in range(x+1, len(selected_tickers)):
            # display ticker in next column
            with columns[(x+y-1)%3]:
                st.metric(label=(selected_tickers[x] + "/" + selected_tickers[y]), value=f"{correlation_data.loc[selected_tickers[x], selected_tickers[y]]:.4}")
    
    # pass correlation data into heatmap generator
    correlation_heatmap(correlation_data)

def correlation_heatmap(data):
    st.header("Correlation Heatmap")
    st.write("A diverse portfolio will have lower correlation, reducing risk of multiple losses at once. The darker the heatmap below, the less correlated the selected assets are.")
    plot = sns.heatmap(data=data, center=0, xticklabels=True, yticklabels=True, annot=True)
    st.pyplot(plot.get_figure())
    plt.close()

def unweighted_returns(pct_data):
    st.header("Daily Portfolio Returns (Equal Weighting)")
    weighted_data = pct_data.mean(axis='columns')
    weighted_returns(pct_data, weighted_data)

def get_weights(pct_data):
    st.header('Daily Portfolio Returns (Weighted Assets)')
    st.write('Type desired weighting of each asset below, as a percentage out of 100.')
    columns = st.columns(3)
    error = st.empty()
    weights = []

    # create as many input boxes as tickers that take input from 0 to 100
    for ticker in selected_tickers:
        with columns[(selected_tickers.index(ticker))%3]:
            weights.append(st.number_input(label=ticker, min_value=0, max_value=100, step=1, key=ticker))
    # call function to check if weights sum to 100
    check_weights(weights, pct_data, error)
    
def check_weights(weights, pct_data, error):
    # if weights sum to 100, proceed to calculating/displaying weighted returns
    sum = 0
    for weight in weights:
        sum += weight
    if sum == 100:
        error.empty()

        # sum all columns according to weighting
        weighted_data = pct_data.dot(np.array(weights)/100)

        # call function to show data
        weighted_returns(pct_data, weighted_data)
    else:
        error.write('Weights must add up to 100.')

def weighted_returns(pct_data, weighted_data):

    # display returns plot
    st.write("**Individual Daily Returns** best viewed over shorter periods of time. For longer timeframes, consult **Cumulative Returns** below.")
    col1, col2 = st.columns([0.7, 0.3])
    plot = sns.lineplot(data=weighted_data, color='orange')
    plot.set(xlabel='Date', ylabel='Daily Return (%)')
    col1.pyplot(plot.get_figure())
    plt.close()
    # display returns in table
    col2.dataframe(weighted_data.to_frame().style.applymap(colors).format("{:.2%}"))

    # total cum. returns
    cum_returns = (weighted_data+1).cumprod()
    # individual cum. returns
    ind_data = (pct_data+1).cumprod()
    # add to plot
    plot, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=ind_data, linewidth=0.7, ax=ax)
    sns.lineplot(data=cum_returns, linewidth=1.4, color='red', ax=ax, label='Portfolio')
    ax.legend()
    ax.set(xlabel='Date', ylabel='Cumulative Return (%)')
    # show plot
    st.header("Cumulative Returns")
    st.write("Below are the returns expected from the selected portfolio over the selected timeframe.")
    st.pyplot(plot.get_figure())
    plt.close()
    # total cum. return metric
    pct_growth = (f"{cum_returns.iloc[-1]:.2%}")
    st.metric(value=pct_growth, label='Total Percentage Growth')
    
# check for submission and run page

st.write("This page analyses all assets' performance and provides conjugate portfolio data. To view individual asset performance, select the 'Individual Analysis' tab.")

if "start" in st.session_state and st.session_state["start"]:
    selected_tickers = st.session_state["selected_tickers"]
    selected_time = st.session_state["selected_time"]
    display()
else:
    st.subheader("Select details on sidebar to view data.")