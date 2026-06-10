# S&P 500 Momentum Strategy

A cross-sectional momentum backtest built in Python, applied to the top 50 S&P 500 constituents by index weight. Based on the Jegadeesh & Titman (1993) 12-1 month formation period framework.

---

## Strategy Overview

At the end of each month:
1. Calculate each stock's 12-1 month return (12 months back, skip most recent month to avoid short-term reversal)
2. Rank all stocks by that return
3. Go equally long the top 10 stocks
4. Hold for 1 month, then rebalance

---

## Project Structure

```
momentum/
├── personal/
│   ├── momentum.py              # Main strategy script
│   └── sp500_top50_tickers.csv  # Universe of 50 tickers by S&P 500 weight
└── README.md
```

---

## Requirements

```bash
pip install pandas yfinance numpy matplotlib
```

---

## Usage

```bash
python momentum.py
```

Outputs:
- Annualized Sharpe ratio
- Total return
- Max drawdown
- Plot of strategy vs. equal-weight buy-and-hold benchmark

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `FORMATION_MONTHS` | 12 | Lookback window for momentum signal |
| `SKIP_MONTHS` | 1 | Months skipped before signal (reversal avoidance) |
| `HOLDING_MONTHS` | 1 | Rebalance frequency |
| `TOP_N` | 10 | Number of stocks held long |
| `START` | 2015-01-01 | Backtest start date |
| `END` | 2026-01-01 | Backtest end date |

---

## Known Limitations

- **Survivorship bias** - universe is today's top 50, not point-in-time constituents
- **No transaction costs** - slippage and commissions not modeled
- **Small universe** - 50 stocks vs. full S&P 500
- **No short side** - long-only implementation

---

## References

- Jegadeesh, N. & Titman, S. (1993). *Returns to Buying Winners and Selling Losers.* Journal of Finance.
- Data sourced via [yfinance](https://github.com/ranaroussi/yfinance)
- Universe sourced from [SlickCharts](https://www.slickcharts.com/sp500) (June 2026)
