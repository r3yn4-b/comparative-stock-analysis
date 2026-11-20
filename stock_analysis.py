# import libraries
import pandas as pd
import streamlit as st
from datetime import date

# navbar and pages
st.set_page_config(page_title="Comparative Stock Analysis and Basic Portfolio Metrics", page_icon=":bar_chart:", initial_sidebar_state="expanded")
st.title("📊 Comparative Stock Analysis and Basic Portfolio Metrics")

pages = [st.Page('pages/individual_analysis.py', title='📈 Individual Analysis'), st.Page('pages/portfolio_analysis.py', title='📈 Portfolio Analysis'), st.Page('pages/markowitz_optimisation.py', title='📈 Markowitz Optimisation')]
st.navigation(pages).run()

st.sidebar.title("Portfolio Details")
st.sidebar.write("All data is requested from Yahoo Finance.")


# initialise session state values
if "start" not in st.session_state:
    st.session_state["start"] = False
if "selected_time" not in st.session_state:
    st.session_state["selected_time"] = None
if "selected_tickers" not in st.session_state:
    st.session_state["selected_tickers"] = None
if "visited" not in st.session_state:
    st.session_state["visited"] = True
if "change_start" not in st.session_state:
    st.session_state["change_start"] = True

# allow re-submit only if ticker or timeframe changes
def resubmit():
    st.session_state["change_start"] = True

# add ticker select as a dropdown
default_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM", "KO", "XOM", "TSLA", "PG", "NVDA", "V", "UNH", "LLY"]
st.session_state["selected_tickers"] = st.sidebar.multiselect('Select Tickers', default_options, accept_new_options=True, max_selections=5, on_change=resubmit)

# start date and end date
end = date.today()
start = (end - pd.DateOffset(years = 5)).date()
st.session_state["selected_time"] = st.sidebar.slider('Timeframe', value=(start, end), on_change=resubmit)

if st.sidebar.button(label= "Display Data", disabled=(not st.session_state["change_start"])) and st.session_state["selected_time"] != None and st.session_state["selected_tickers"] != None:
    st.session_state["start"] = True
    st.session_state["change_start"] = False
else:
    # if either timeframe or tickers change, allow resubmission of data
    st.session_state["change_start"] = True



