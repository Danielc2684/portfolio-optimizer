Portfolio Optimization with Live Market Data

This project uses real market data to build an **optimized investment portfolio** using Python.  
It applies **Modern Portfolio Theory (MPT)** — created by Harry Markowitz — to find the best combination of assets that maximizes return for a given level of risk.

The goal is simple:  
> Find the most efficient mix of assets that gives the highest **Sharpe ratio** (risk-adjusted return).

---

##  What This Project Does

This Python script:
1. Downloads 1 year of daily price data for selected assets (`QQQ`, `SPY`, `GLD`, and `NQ=F`) using **Yahoo Finance**.
2. Calculates **logarithmic returns** (which represent continuous compounding).
3. Builds an **annualized covariance matrix** to measure how assets move together.
4. Retrieves the **10-Year U.S. Treasury Yield** from the **Federal Reserve (FRED)** to use as the **risk-free rate**.
5. Uses **numerical optimization** to find the optimal asset weights that maximize the **Sharpe ratio**, while applying realistic constraints:
   - Total weights = 1  
   - No short selling  
   - Max 50% allocation per asset
6. Displays the results — expected annual return, volatility, and Sharpe ratio — along with a bar chart of optimal weights.

---

## Tools Used

- **Python 3.10+**
- `pandas` → Data manipulation  
- `NumPy` → Math and matrix operations  
- `yfinance` → Real-time financial data  
- `fredapi` → Economic data (risk-free rate)  
- `SciPy` → Optimization (`SLSQP` solver)  
- `Matplotlib` → Visualizations  