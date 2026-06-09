import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt


''' 
Personal

stocks = pd.read_csv("sp500_top50_tickers.csv")
tickers = stocks["ticker"].tolist()
tickers = [t.replace(".", "-") for t in tickers]

df = yf.download(tickers, period="1y", auto_adjust=True)["Close"]
print(df.shape)
'''

# download stock
ticker = 'MSFT'
data = yf.download(ticker, start='2015-01-01', end='2026-01-01', auto_adjust = True)

# calculate short term and long term moving average
data['Short_MA'] = data['Close'].rolling(window=10).mean() #10-day moving average
data['Long_MA'] = data['Close'].rolling(window=50).mean() #50-day moving average

# create signals for buy and sell
data['Signal'] = 0 # default, no position
data.loc[data.index[10:], 'Signal'] = np.where(
    data['Short_MA'].iloc[10:] > data['Long_MA'].iloc[10:], 1, -1
) # 1 for Buy, -1 for Sell

print(data[['Short_MA', 'Long_MA', 'Signal']].tail())

# Calculate daily returns
data['Returns'] = data['Close'].pct_change()

# Calculate strategy returns
data['Strategy_Returns'] = data['Returns'] * data['Signal'].shift(1)

# Calculate cumulative returns for the strategy and for buy-and-hold
data['Cumulative_Strategy_Returns'] = (1 + data['Strategy_Returns']).cumprod()
data['Cumulative_Buy_and_Hold'] = (1 + data['Returns']).cumprod()

# View the performance
print(data[['Cumulative_Strategy_Returns', 'Cumulative_Buy_and_Hold']].tail())

# plot performance vs buy and hold
plt.figure(figsize=(10, 6))
plt.plot(data['Cumulative_Strategy_Returns'], label='Strategy Returns', color='g')
plt.plot(data['Cumulative_Buy_and_Hold'], label='Buy and Hold Returns', color='b')
plt.title(f'{ticker} Momentum Strategy Performance')
plt.legend()
plt.show()




