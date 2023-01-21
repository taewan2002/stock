from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import datetime
import time
import os

# class makePortfolio:
#     def __init__(self, tickers):
#         self.tickers = tickers
#
#     def getportfolio(self):
#         yf.pdr_override()
#         start = datetime.datetime(2019, 1, 1)
#         end = datetime.datetime(2020, 1, 1)
#         df = pdr.get_data_yahoo(self.tickers, start, end)
#         return df



# Portfolio Optimization 포트폴리오 최적화
# 샤프지수 = (포트폴리오 예상 수익률 - 무위험률) / 수익률의 표준편차
df = pd.DataFrame()
yf.pdr_override()
stocks = ["AAPL", "GOOGL", "TSLA", "NVDA", "MSFT", "AMZN", "AMD", "ASML", "BRK-B", "UNH", "JNJ", "META", "O", "BLK", "RBLX"]
for i in stocks:
    df[i] = pdr.get_data_yahoo(i, start="2010-01-01", progress = False)['Close']

daily_ret = df.pct_change() # 일간 변동률
annual_ret = daily_ret.mean() * 252 # 연간 수익률
daily_cov = daily_ret.cov() # 일간 리스크
annual_cov = daily_cov * 252 # 연간 리스크

port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []
num_assets = len(stocks)
num_portfolios = 100000

for portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
    sharpe = returns / risk
    sharpe_ratio.append(sharpe)
    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}

for counter, symbol in enumerate(stocks):
    portfolio[symbol] = [Weight[counter] for Weight in port_weights]

df = pd.DataFrame(portfolio)
column_order = ['Returns', 'Risk', 'Sharpe'] + [stock for stock in stocks]
df = df[column_order]

# 5단계의 포트폴리오 최적화

max_sharp = df.loc[df['Sharpe'] == df['Sharpe'].max()]
min_risk = df.loc[df['Risk'] == df['Risk'].min()]
print(max_sharp)
print(min_risk)