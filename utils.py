# shared helpers used across pages
import yfinance as yf
import streamlit as st

# fetch data using yahoo finance API

@st.cache_data
def fetch_data(tickers: tuple, timeframe: tuple):
    data = yf.download(tickers, start = timeframe[0], end = timeframe[1])['Close'].sort_index()
    return data

# changes data value colors

def colors(value):
    if value > 0:
        color = 'green'
    elif value < 0:
        color = 'red'
    else:
        color = 'grey'
    return f'color: {color};'
