# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import fetch_data
from scipy.optimize import minimize
from datetime import date

st.title("📈 Markowitz Optimisation")

def display():
    try:
        with st.spinner("Downloading data..."):
            data = fetch_data(selected_tickers, selected_time)
            pct_data = data.pct_change().dropna()
            risk_free = get_rfr(selected_time)
        if data.empty:
            st.write("Invalid request. Check tickers or date range.")
        elif len(data.columns) < 2:
            st.write("To display portfolio metrics, at least two tickers must be selected.")
        else:
            # calculate data
            ann_returns, ann_cov = annualise_data(pct_data)
            portfolios, weights_df = monte_carlo(ann_returns, ann_cov, risk_free, selected_tickers)
            best_vol_weights = find_best_vol(portfolios, weights_df)
            best_vol_weights, min_volatility = min_vol(best_vol_weights, ann_cov)
            best_sharpe_weights = find_best_sharpe(portfolios, weights_df)
            best_sharpe_weights, max_sharpe_ratio = max_sharpe(best_sharpe_weights, ann_returns, ann_cov, risk_free)

            # display data
            efficient_frontier(portfolios, weights_df)
            show_optimal(best_vol_weights, min_volatility, best_sharpe_weights, max_sharpe_ratio, risk_free, ann_returns, ann_cov)
    except:
        st.subheader("Must select one or more tickers to display.")

# get risk free rate using TBIL

def get_rfr(selected_time):
    # fetch treasury data if available in given timeframe
    # if not in range, return fallback value
    if selected_time[0] < date(2022,8,9):
        return 0.02
    else:
        treasury_data = fetch_data('TBIL', selected_time)
        return treasury_data.pct_change().dropna().mean() * 252

# annualise ticker data

def annualise_data(pct_data):
    ann_returns = pct_data.mean() * 252
    ann_cov = pct_data.cov() * 252
    return ann_returns, ann_cov

# calculate annualised portfolio returns

def portfolio_return(weights, ann_returns):
    port_return = ann_returns.dot(np.array(weights))
    return port_return

# calculate annualised portfolio volatility

def portfolio_vol(weights, ann_cov):
    port_vol = np.sqrt(np.dot(np.transpose(weights), np.dot(ann_cov, weights)))
    return port_vol
    
# calculate portfolio sharpe ratio

def portfolio_sharpe(port_return, port_vol, risk_free):
    sharpe = (port_return - risk_free)/port_vol
    return sharpe

# function to return negative sharpe value for optimisation function

def optimise_sharpe(weights, ann_returns, ann_cov, risk_free):
    ret = portfolio_return(weights, ann_returns)
    vol = portfolio_vol(weights, ann_cov)

    return -portfolio_sharpe(ret, vol, risk_free)

# populate table with metrics of 50,000 portfolios of randomised weights

@st.cache_data
def monte_carlo(ann_returns, ann_cov, risk_free, selected_tickers):
    returns = []
    volatility = []
    sharpe = []
    weights_arr = []

    for model in range(50000):
        # generate random numbers
        weights = np.random.random(len(selected_tickers))
        # convert to weights
        weights /= np.sum(weights)
        # calculate metrics
        # add to separate arrays
        ret_val = portfolio_return(weights, ann_returns)
        returns.append(ret_val)
        vol_val = portfolio_vol(weights, ann_cov)
        volatility.append(vol_val)
        sharpe.append(portfolio_sharpe(ret_val, vol_val, risk_free))
        weights_arr.append(weights)

    # add lists to form portfolio dataframe
    portfolios = pd.DataFrame(data={'Returns': returns, 'Volatility': volatility, 'Sharpe Ratio': sharpe})
    weights_df = pd.DataFrame(weights_arr, columns=selected_tickers)
    return portfolios, weights_df

# best starting weights for minimum volatility

def find_best_vol(portfolios, weights_df):
    best_idx = portfolios.loc[:,'Volatility'].idxmin()
    best_weights = weights_df.loc[best_idx, :].to_numpy()
    return best_weights

# find optimised weights for minimum volatility
 
def min_vol(weights, ann_cov):
    result = minimize(portfolio_vol, x0=weights, args=(ann_cov,), method='SLSQP', bounds=tuple((0,1) for ticker in range(len(selected_tickers))), constraints={'type':'eq', 'fun': lambda weights: np.sum(weights)-1})
    best_weights = result.x
    min_volatility = portfolio_vol(best_weights, ann_cov)
    return best_weights, min_volatility

# best starting weights for maximum sharpe ratio

def find_best_sharpe(portfolios, weights_df):
    best_idx = portfolios.loc[:,'Sharpe Ratio'].idxmax()
    best_weights = weights_df.loc[best_idx, :].to_numpy()
    return best_weights

# find optimised weights for maximum sharpe ratio

def max_sharpe(weights, ann_returns, ann_cov, risk_free):
    result = minimize(optimise_sharpe, x0=weights, args=(ann_returns, ann_cov, risk_free), method='SLSQP', bounds=tuple((0,1) for ticker in range(len(selected_tickers))), constraints={'type':'eq', 'fun': lambda weights: np.sum(weights)-1})
    # return negative of minimum value, to return the maximum value
    best_weights = result.x
    port_return = portfolio_return(best_weights, ann_returns)
    port_vol = portfolio_vol(best_weights, ann_cov)
    max_sharpe_ratio = portfolio_sharpe(port_return, port_vol, risk_free)
    return best_weights, max_sharpe_ratio
    
# display monte carlo data and plot the efficient frontier for maximum return (y) for each given risk (x)

def efficient_frontier(portfolios, weights_df):
    st.header('Efficient Frontier')
    st.write('The efficient frontier visualises the optimal portfolio weightings, as guidance to the maximum return at each risk level.')
    portfolios.loc[:, 'Returns'] *= 100
    fig, ax = plt.subplots()
    plot = ax.scatter(data=portfolios, x='Volatility', y='Returns', c=portfolios['Sharpe Ratio'], cmap='viridis')
    plt.colorbar(mappable=plot, ax=ax, label='Sharpe Ratio')
    ax.set_ylabel('Return (%)')
    st.pyplot(fig)
    plt.close()

    st.subheader('Maximise Return for Specified Volatility')
    st.write('This provides the optimal weights to maximise return at the chosen volatility.')
    portfolios = round(portfolios, 3)
    selected_vol = st.select_slider('Select Volatility:', options=(portfolios.sort_values('Volatility').loc[:,'Volatility']))

    index = portfolios[portfolios['Volatility'] == selected_vol]['Returns'].idxmax()
    weights = weights_df.loc[index]

    num = 0
    columns = st.columns(3)
    for ticker in selected_tickers:
        with columns[num%3]:
            st.metric(ticker, f"{weights.loc[ticker]:.2%}")
        num += 1

    st.write('Weighting percentages may not add up to 100 due to rounding.')

# display optimal weights for minimum volatility and maximum sharpe ratio

def show_optimal(best_vol_weights, min_volatility, best_sharpe_weights, max_sharpe_ratio, risk_free, ann_returns, ann_cov):
    st.header('Minimum Annualised Volatility')
    st.write('The following asset weighting:')

    num = 0
    columns = st.columns(3)
    for i in range(len(selected_tickers)):
        with columns[num%3]:
            st.metric(selected_tickers[i], round(best_vol_weights[i], 2))
        num += 1

    st.write('Will produce the lowest volatility portfolio, with metrics:')
    
    num = 0
    columns = st.columns(3)
    temp_returns = portfolio_return(best_vol_weights, ann_returns)
    columns[0].metric('Annualised Return', round(temp_returns, 3))
    columns[1].metric('Annualised Volatility', round(min_volatility, 3))
    columns[2].metric('Sharpe Ratio', round(portfolio_sharpe(temp_returns, min_volatility, risk_free), 3))

    st.header('Maximum Sharpe Ratio')
    st.write('The following asset weighting:')

    num = 0
    columns = st.columns(3)
    for i in range(len(selected_tickers)):
        with columns[num%3]:
            st.metric(selected_tickers[i], round(best_sharpe_weights[i],2))
        num += 1

    st.write('Will produce the portfolio with the highest Sharpe Ratio, with metrics:')
    
    num = 0
    columns = st.columns(3)
    columns[0].metric('Annualised Return', round(portfolio_return(best_sharpe_weights, ann_returns), 3))
    columns[1].metric('Annualised Volatility', round(portfolio_vol(best_sharpe_weights, ann_cov), 3))
    columns[2].metric('Sharpe Ratio', round(max_sharpe_ratio, 3))
  
if "start" in st.session_state and st.session_state["start"]:
    selected_tickers = st.session_state["selected_tickers"]
    selected_time = st.session_state["selected_time"]
    display()
else:
    st.subheader("Select details on sidebar to view data.")