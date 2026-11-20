# Comparative Stock Analysis & Portfolio Optimisation

An interactive Streamlit web app for comparing up to five stocks, analysing how a portfolio of them would have performed, and finding optimal portfolio weightings using Markowitz mean-variance optimisation. All market data is pulled live from Yahoo Finance.

<!-- Add a screenshot or GIF of the app here, e.g. ![App screenshot](docs/screenshot.png) -->

## Features

The app has three pages, all driven by one shared sidebar where you pick tickers and a date range.

### 📈 Individual Analysis
- Historic closing-price trends for each selected asset
- Per-asset metrics: average daily return, daily and annualised volatility, and total cumulative return
- Daily-return tables with colour-coded gains and losses
- Return-distribution histograms with KDE curves to compare volatility visually

### 📈 Portfolio Analysis
- Daily and cumulative returns for an equal-weighted portfolio
- Custom portfolio weights entered by the user, checked so they sum to 100%
- Cumulative portfolio growth plotted against each individual asset
- Pairwise Pearson correlation coefficients and a correlation heatmap

### 📈 Markowitz Optimisation
- Monte Carlo simulation of 50,000 randomly weighted portfolios
- Efficient frontier plot coloured by Sharpe ratio
- Interactive slider showing the highest-return weighting at a chosen volatility
- Numerically optimised (SciPy SLSQP) weights for:
  - the **minimum-volatility** portfolio
  - the **maximum-Sharpe-ratio** portfolio
- Risk-free rate estimated from the `TBIL` US Treasury bill ETF where data is available, with a 2% fallback for earlier periods

## Tech stack

| Area | Tools |
|---|---|
| Web app | Streamlit (multipage navigation, session state, caching) |
| Data | yfinance, pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Optimisation | SciPy (`scipy.optimize.minimize`) |

## Getting started

**Requirements:** Python 3.12 or later.

```bash
# 1. Clone the repository
git clone https://github.com/r3yn4-b/comparative-stock-analysis.git
cd comparative-stock-analysis

# 2. (Recommended) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run stock_analysis.py
```

The app opens at `http://localhost:8501`.

## How to use

1. In the sidebar, pick up to five tickers from the list or type your own (any symbol Yahoo Finance recognises).
2. Set the date range with the **Timeframe** slider. It defaults to the last five years.
3. Click **Display Data**.
4. Move between **Individual Analysis**, **Portfolio Analysis** and **Markowitz Optimisation** using the navigation menu. The portfolio and optimisation pages need at least two tickers.

## Project structure

```
comparative-stock-analysis/
├── stock_analysis.py              # Entry point: page config, navigation, shared sidebar inputs
├── utils.py                       # Shared helpers: cached Yahoo Finance download, table colouring
├── pages/
│   ├── individual_analysis.py     # Per-asset prices, metrics and return distributions
│   ├── portfolio_analysis.py      # Equal/custom-weighted portfolio returns and correlation
│   └── markowitz_optimisation.py  # Monte Carlo efficient frontier and SLSQP optimisation
├── requirements.txt
└── README.md
```

## Methodology notes

- **Daily returns:** percentage change in closing price.
- **Annualisation:** 252 trading days. Annual volatility is `σ_daily × √252`, and annual returns and covariance are scaled by 252.
- **Portfolio volatility:** `√(wᵀ Σ w)`, where `Σ` is the annualised covariance matrix.
- **Sharpe ratio:** `(R_p − R_f) / σ_p`.
- **Optimisation constraints:** weights are long-only (between 0 and 1) and sum to 1.

## Limitations

- Results are based purely on historical data, and past performance does not predict future returns.
- Mean-variance optimisation is sensitive to its inputs: small changes in the date range can shift the optimal weights a lot.
- The analysis ignores transaction costs, taxes and short selling.

## Disclaimer

This project is for educational purposes only and is not financial advice.
