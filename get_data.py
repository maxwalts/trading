import requests
import pandas as pd


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
    timestamps = [price_data[0] // 1000 for price_data in data['prices']]  # Convert to seconds
    return pd.DataFrame({'timestamp': timestamps, 'price': prices})