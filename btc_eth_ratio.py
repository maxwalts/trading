import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from get_data import get_hourly_prices, get_daily_prices, process_data


# NOTE: max number of days is 90 for hourly data.
def generate_plot(timeframe='hourly', days=90):
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


if __name__ == '__main__':
    generate_plot('hourly', 90)
    generate_plot('daily', 365)