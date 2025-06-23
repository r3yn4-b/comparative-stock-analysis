# import libraries
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import timedelta, date

st.title("📈 Portfolio Metrics")

if "start" in st.session_state and st.session_state["start"]:
    selected_tickers = st.session_state["selected_tickers"]
    selected_time = st.session_state["selected_time"]
else:
    st.write("Select details on sidebar to view data.")