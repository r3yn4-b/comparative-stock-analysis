# import libraries
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import timedelta, date

# navbar and pages
st.set_page_config(page_title="Comparative Stock Analysis and Basic Portfolio Metrics", page_icon=":bar_chart:", initial_sidebar_state="expanded")
st.title("📊 Comparative Stock Analysis and Basic Portfolio Metrics")

pages = [st.Page('individual_analysis.py', title='Individual Analysis'), st.Page('portfolio_metrics.py', title='Portfolio Metrics')]
page = st.navigation(pages)
page.run()

st.set_page_config(page_title="Comparative Stock Analysis and Basic Portfolio Metrics", page_icon=":bar_chart:", initial_sidebar_state="expanded")
st.sidebar.title("Portfolio Details")

# initialise session state values
st.session_state["start"] = False
st.session_state["selected_time"] = None
st.session_state["selected_tickers"] = None
st.session_state["visited"] = True


# add ticker select as a dropdown
default_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM", "KO", "XOM", "TSLA", "PG", "NVDA", "V", "UNH", "LLY"]
st.session_state["selected_tickers"] = st.sidebar.multiselect('Select Tickers', default_options, accept_new_options=True, max_selections=5)

# start date and end date

end = date.today()
start = (end - pd.DateOffset(years = 5)).date()
st.session_state["selected_time"] = st.sidebar.slider('Timeframe', value=(start, end))
if st.sidebar.button("Display Data") and st.session_state["selected_time"] != None and st.session_state["selected_tickers"] != None:
    st.session_state["start"] = True



