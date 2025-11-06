import yfinance as yf
import pandas as pd 
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize

tickers = ['QQQ', 'SPY', 'GLD', 'NQ=F']
print(tickers)

end_date = datetime.today()
print(end_date)

start_date = end_date - timedelta(days = 365)
print(start_date)

adj_close_df = pd.DataFrame()

for ticker in tickers:
    data = yf.download(ticker, start = start_date, end = end_date, auto_adjust = True, progress = False)
    adj_close_df[ticker] = data['Close']
print(adj_close_df)

logreturns = np.log(adj_close_df / adj_close_df.shift(1)).dropna()
print(logreturns)

cov_matrix = logreturns.cov()*252
print(cov_matrix)

def standard_deviation(weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)

def expected_return(weights, logreturns):
    return np.sum(logreturns.mean()*weights)*252

def sharp_ratio(weights, logreturns, cov_matrix, risk_free_rate):
    return(expected_return(weights, logreturns) - risk_free_rate) / standard_deviation(weights, cov_matrix)

from fredapi import Fred

fred = Fred(api_key ='3e2255ed38b061195fd85b081d2e7e6b')
ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100
risk_free_rate = ten_year_treasury_rate.iloc[-1]
print(risk_free_rate)

def neg_sharp_ratio(weights, logreturns, cov_matrix, risk_free_rate):
    return -sharp_ratio(weights, logreturns, cov_matrix, risk_free_rate)

constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
bounds = [(0, 0.5) for _ in range(len(tickers))]

initial_weights = np.array([1/len(tickers)]*len(tickers))
print(initial_weights)

optimized_results = minimize(neg_sharp_ratio, initial_weights, args=(logreturns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
optimal_weights = optimized_results.x

print("Optimal Weights:")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight: .4f}")

print()

optimal_portfolio_return = expected_return(optimal_weights, logreturns)
optimal_portfolio_volitility = standard_deviation(optimal_weights,cov_matrix)
optimal_sharpe_ratio = sharp_ratio(optimal_weights, logreturns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimal_portfolio_return:.4f}")
print(f"Expected Volitility: {optimal_portfolio_volitility:.4f}")
print(f"Sharpe Ratio: {optimal_sharpe_ratio:.4f}")

import matplotlib.pyplot as plt

plt.figure(figsiz=(10,6))
plt.bar(tickers, optimal_weights)

plt.xlabel('Assets')
plt.ylabel('Optimal Weights')
plt.title('Optimal Portfolio Weights')

plt.show()