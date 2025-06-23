import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date
import numpy as np

def calculate_metrics(data):
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
    return metrics

def fetch_data(tickers: tuple, timeframe: tuple):
    data = yf.download(tickers, start = timeframe[0], end = timeframe[1])['Close'].sort_index()
    return data

data = fetch_data(['JPM', 'KO'], (date(2021, 12, 9), date(2023, 10, 25)))
print(data)