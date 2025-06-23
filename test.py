import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date

appl = yf.download('MSFT', start = date(2020, 6, 23), end = date(2025, 6, 23))
print(appl.loc[:, 'Close'])