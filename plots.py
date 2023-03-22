import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from get_data import get_hourly_prices, get_daily_prices, process_data


def plot_portfolio_value(price_strategy_df):
    # plot portfolio value, USD balance and buy/sell signals
    plt.figure(figsize=(12, 6))
    plt.plot(price_strategy_df['timestamp'], price_strategy_df['portfolio_value'], label='Portfolio Value')
    # plot USD balance
    plt.plot(price_strategy_df['timestamp'], price_strategy_df['usd_balance'], label='USD Balance')
    # plot change in close price (start with 0)
    plt.plot(price_strategy_df['timestamp'], price_strategy_df['close'].diff(), label='Change in Close Price')

    # plot Buy and Sell signals

    plt.scatter(price_strategy_df[price_strategy_df['buy_signal']]['timestamp'],
                price_strategy_df[price_strategy_df['buy_signal']]['portfolio_value'],
                marker='^', color='green', s=10, label='Buy Signal')
    plt.scatter(price_strategy_df[price_strategy_df['sell_signal']]['timestamp'],
                price_strategy_df[price_strategy_df['sell_signal']]['portfolio_value'],
                marker='v', color='red', s=10, label='Sell Signal')

    plt.legend()
    plt.xlabel('Timestamp')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.xticks(rotation=45)

    # date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    # plt.gca().xaxis.set_major_formatter(date_formatter)
    # plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.show()


# NOTE: max number of days is 90 for hourly data.
def plot_ratio(timeframe='hourly', days=90):
    if timeframe == 'hourly':
        bitcoin_data = get_hourly_prices('bitcoin', days)
        ethereum_data = get_hourly_prices('ethereum', days)
    elif timeframe == 'daily':
        bitcoin_data = get_daily_prices('bitcoin', days)
        ethereum_data = get_daily_prices('ethereum', days)
    else:
        raise ValueError("Invalid timeframe. Choose either 'hourly' or 'daily'.")

    bitcoin_df = process_data(bitcoin_data)
    ethereum_df = process_data(ethereum_data)

    merged_df = bitcoin_df.merge(ethereum_df, on='timestamp', suffixes=('_btc', '_eth'))
    merged_df['ratio'] = merged_df['price_btc'] / merged_df['price_eth']

    merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'], unit='s')

    plt.figure(figsize=(12, 6))
    plt.plot(merged_df['timestamp'], merged_df['ratio'])
    plt.xlabel('Timestamp')
    plt.ylabel('BTC/ETH Price Ratio')
    plt.title(f'{timeframe.capitalize()} BTC/ETH Price Ratio for the Last {days} Days')
    plt.xticks(rotation=45)

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.show()


# plot the price of bitcoin and ethereum over the last 90 days
def plot_prices(timeframe='hourly', days=90):
    if timeframe == 'hourly':
        bitcoin_data = get_hourly_prices('bitcoin', days)
        ethereum_data = get_hourly_prices('ethereum', days)
    elif timeframe == 'daily':
        bitcoin_data = get_daily_prices('bitcoin', days)
        ethereum_data = get_daily_prices('ethereum', days)
    else:
        raise ValueError("Invalid timeframe. Choose either 'hourly' or 'daily'.")

    bitcoin_df = process_data(bitcoin_data)
    ethereum_df = process_data(ethereum_data)

    bitcoin_df['timestamp'] = pd.to_datetime(bitcoin_df['timestamp'], unit='s')
    ethereum_df['timestamp'] = pd.to_datetime(ethereum_df['timestamp'], unit='s')

    plt.figure(figsize=(12, 6))
    plt.plot(bitcoin_df['timestamp'], bitcoin_df['price'], label='Bitcoin')
    plt.plot(ethereum_df['timestamp'], ethereum_df['price'], label='Ethereum')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.title(f'{timeframe.capitalize()} Price of Bitcoin and Ethereum for the Last {days} Days')
    plt.xticks(rotation=45)

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.legend()
    plt.grid(True)
    plt.show()

def plot_portfolio_value(price_strategy_df):
    plt.figure(figsize=(12, 6))
    plt.plot(price_strategy_df['timestamp'], price_strategy_df['portfolio_value'])
    plt.xlabel('Timestamp')
    plt.ylabel('Portfolio Value')
    plt.title(f'Portfolio Value Over Time')
    plt.xticks(rotation=45)

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    
    plot_ratio('hourly', 90)
    plot_prices('hourly', 90)
    # generate_plot('daily', 365)