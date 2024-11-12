import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

def calculate_moving_averages(data, short_window=20, long_window=50):
    data['SMA20'] = data['Close'].rolling(window=short_window).mean()
    data['SMA50'] = data['Close'].rolling(window=long_window).mean()
    return data

def generate_signals(data):
    data['Signal'] = 0.0
    data['Signal'][20:] = np.where(data['SMA20'][20:] > data['SMA50'][20:], 1.0, 0.0)
    data['Position'] = data['Signal'].diff()
    return data

if __name__ == "__main__":
    ticker = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    stock_data = get_stock_data(ticker, start_date, end_date)
    stock_data = calculate_moving_averages(stock_data)
    stock_data = generate_signals(stock_data)

    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Close'], label='Close Price', alpha=0.5)
    plt.plot(stock_data['SMA20'], label='20-day SMA', alpha=0.75)
    plt.plot(stock_data['SMA50'], label='50-day SMA', alpha=0.75)
    plt.scatter(stock_data.index, stock_data['Position'] == 1, color='green', label='Buy Signal', marker='^', alpha=1)
    plt.scatter(stock_data.index, stock_data['Position'] == -1, color='red', label='Sell Signal', marker='v', alpha=1)
    plt.title('Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
