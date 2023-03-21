import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Get hourly prices for Bitcoin and Ethereum (last 90 days)
def get_hourly_prices(crypto_id, days):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'hourly'
    }
    response = requests.get(url, params=params)
    print(f'API response code: {response.status_code}')
    # print(response.headers)
    return response.json()

def get_daily_prices(crypto_id, days):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    print(f'API response code: {response.status_code}')
    # print(response.headers)
    return response.json()

# Process data and create a pandas DataFrame
def process_data(data):
    prices = [price_data[1] for price_data in data['prices']]
    timestamps = [price_data[0] // 1000 for price_data in data['prices']] # Convert to seconds
    return pd.DataFrame({'timestamp': timestamps, 'price': prices})


def generate_hourly_plot(days=90):
    bitcoin_data = get_hourly_prices('bitcoin', days)
    ethereum_data = get_hourly_prices('ethereum', days)

    bitcoin_df = process_data(bitcoin_data)
    ethereum_df = process_data(ethereum_data)

    # Merge data and calculate the ratio
    merged_df = bitcoin_df.merge(ethereum_df, on='timestamp', suffixes=('_btc', '_eth'))
    merged_df['ratio'] = merged_df['price_btc'] / merged_df['price_eth']

    # Convert UNIX timestamps to datetime objects
    merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'], unit='s')

    # Plot the ratio
    plt.figure(figsize=(12, 6))
    plt.plot(merged_df['timestamp'], merged_df['ratio'])
    plt.xlabel('Timestamp')
    plt.ylabel('BTC/ETH Price Ratio')
    plt.title(f'Hourly BTC/ETH Price Ratio for the Last {days} Days')
    plt.xticks(rotation=45)

    # Customize the x-axis to display human-readable dates
    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    # Add grid lines and show plot
    plt.grid(True)
    plt.show()


def generate_daily_plot(days=90):
    # plot the daily prices
    bitcoin_data = get_daily_prices('bitcoin', days)
    ethereum_data = get_daily_prices('ethereum', days)

    bitcoin_df = process_data(bitcoin_data)
    ethereum_df = process_data(ethereum_data)

    merged_df = bitcoin_df.merge(ethereum_df, on='timestamp', suffixes=('_btc', '_eth'))
    merged_df['ratio'] = merged_df['price_btc'] / merged_df['price_eth']

    merged_df['timestamp'] = pd.to_datetime(merged_df['timestamp'], unit='s')

    plt.figure(figsize=(12, 6))
    plt.plot(merged_df['timestamp'], merged_df['ratio'])
    plt.xlabel('Timestamp')
    plt.ylabel('BTC/ETH Price Ratio')
    plt.title(f'Daily BTC/ETH Price Ratio for the Last {days} Days')
    plt.xticks(rotation=45)

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    generate_daily_plot(365*4)