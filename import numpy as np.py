import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# ── 1. CONFIG ────────────────────────────────────────────────────────────────
FORMATION_MONTHS = 12
SKIP_MONTHS = 1
HOLDING_MONTHS = 1
TOP_N = 10
START = "2015-01-01"
END = '2026-01-01'

# ── 2. LOAD TICKERS ──────────────────────────────────────────────────────────
stocks = pd.read_csv("sp500_top50_tickers.csv")
tickers = [t.replace(".", "-") for t in stocks["ticker"].tolist()]

# ── 3. DOWNLOAD ADJUSTED PRICES ──────────────────────────────────────────────
raw = yf.download(tickers, start = START, end  = END, auto_adjust = True)["Close"]

# Resample to month-end prices (rebalance monthly)
prices = raw.resample("ME").last()

# ── 4. CALCULATE MOMENTUM SIGNAL ─────────────────────────────────────────────
# 12 - 1 month return: return from 12 months ago to 1 month ago (skip last month)
# At time t, signal = price[t-1] / price[t - 13] - 1
momentum = prices.shift(SKIP_MONTHS) / prices.shift(FORMATION_MONTHS + SKIP_MONTHS)

# ── 5. GENERATE PORTFOLIO WEIGHTS ────────────────────────────────────────────
def get_weights(row):
    """
    At each rebalance date, rank stocks by momentum signal.
    Go equally long the top TOP_N stocks. No short side (long-only).
    Returns a Series of weights for that month.
    """
    valid = row.dropna()
    if len(valid) < TOP_N:
        return pd.Series(0, index=row.index)
    ranked = valid.rank(ascending=False)
    selected = ranked[ranked <= TOP_N].index
    weights = pd.Series(0.0, index=row.index)
    weights[selected] = 1.0 / TOP_N
    return weights
# Apply across all months (shift by 1 to avoid lookahead: signal at t, trade at t+1)
weights = momentum.apply(get_weights, axis=1).shift(1)

# ── 6. CALCULATE RETURNS ─────────────────────────────────────────────────────
# Monthly returns from price data
monthly_returns = prices.pct_change()

# Portfolio return eahc month = sum of (weight * stock return)
portfolio_returns = (weights * monthly_returns).sum(axis=1)

# buy and hold benchmark: equal weight all 50 stocks
bah_returns = monthly_returns.mean(axis=1)

# ── 7. CUMULATIVE RETURNS ────────────────────────────────────────────────────
cum_strategy = (1 + portfolio_returns).cumprod()
cum_bah = (1 + bah_returns).cumprod()

# ── 8. PERFORMANCE METRICS ───────────────────────────────────────────────────
def sharpe(returns, periods=12):
    """Anualized sharpe ratio assuming risk-free rate of 0"""
    return (returns.mean() / returns.std()) * np.sqrt(periods)

def max_drawdown(cum_returns):
    """Maximum peak to trough drawdown"""
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    return drawdown.min()

print("=== Strategy Performance ===")
print(f"Total Return: {cum_strategy.iloc[-1] - 1:.2%}")
print(f"Annualized Sharpe: {sharpe(portfolio_returns):.2%}")
print(f"Max Drawdown: {max_drawdown(cum_strategy):.2%}")

print ("\n=== Buy and Hold Benchmark ===")
print(f"Total Return: {cum_bah.iloc[-1] - 1:.2%}")
print(f"Annualized Sharpe: {sharpe(bah_returns):.2%}")
print(f"Max Drawdown: {max_drawdown(cum_bah):.2%}")

# ── 9. PLOT ───────────────────────────────────────────────────────────────────
plt.figure(figsize=(12,6))
plt.plot(cum_strategy, label='Momentum Strategy (Top 10)', color='g')
plt.plot(cum_bah, label='Equal Weight Buy & Hold', color='b')
plt.title("S&P500 Top 50 - Cross-Sectional Momentum Backtest(2015-2026)")
plt.ylabel('Cumulative Return')
plt.xlabel('Date')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
