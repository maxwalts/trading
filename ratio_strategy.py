import pandas as pd
import numpy as np
import get_data
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# get DF of hourly prices for bitcoin and ethereum for the last 90 days
bitcoin_data = get_data.get_hourly_prices('bitcoin', 90)
ethereum_data = get_data.get_hourly_prices('ethereum', 90)

# convert the data to a pandas dataframe
bitcoin_df = get_data.process_data(bitcoin_data)
ethereum_df = get_data.process_data(ethereum_data)

# convert the timestamp to a datetime object
bitcoin_df['timestamp'] = pd.to_datetime(bitcoin_df['timestamp'], unit='s')
ethereum_df['timestamp'] = pd.to_datetime(ethereum_df['timestamp'], unit='s')

# join the dataframes on timestamp
combined_df = bitcoin_df.merge(ethereum_df, on='timestamp', suffixes=('_BTC', '_ETH'))

# add a column for the ratio of bitcoin to ethereum
combined_df['BTC.ETH'] = combined_df['price_BTC'] / combined_df['price_ETH']

# add a column for the moving average
combined_df['MA_short'] = combined_df['BTC.ETH'].rolling(24).mean()

# add column for the difference between the price and the moving average
combined_df['diff'] = combined_df['BTC.ETH'] - combined_df['MA_short']

# generate buy signal when the price is below the moving average, and sell signal when the price is above the moving average
# 0: sell BTC, buy ETH
# 1: buy BTC, sell ETH
combined_df['signal'] = np.where(combined_df['diff'] > 0, 0, 1)

# drop rows with NaN values
combined_df.dropna(inplace=True)

print(combined_df.head())

# plot the ratio
def plot():
    plt.figure(figsize=(12, 6))
    plt.plot(combined_df['timestamp'], combined_df['BTC.ETH'])
    plt.xlabel('Timestamp')
    plt.ylabel('BTC/ETH Price Ratio')
    plt.title(f'Hourly BTC.ETH for the Last 90 Days with 24 Day Moving Average')
    plt.xticks(rotation=45)

    # add a line for the moving average
    plt.plot(combined_df['timestamp'], combined_df['MA_short'], color='red')

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.show()

# plot the portfolio value over time
def plot_portfolio(df, portfolio):
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], portfolio)
    plt.xlabel('Timestamp')
    plt.ylabel('Portfolio Value')
    plt.title(f'Ratio strategy: Portfolio Value')
    plt.xticks(rotation=45)

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.show()


def plot_holdings(df):
       # plot the holdings of BTC, and ETH over time
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], strategy_result_df['btc_balance'], label='BTC')
    plt.plot(df['timestamp'], strategy_result_df['eth_balance'], label='ETH')
    plt.xlabel('Timestamp')
    plt.ylabel('Balance')
    plt.title(f'Ratio strategy: BTC and ETH Holdings')
    plt.xticks(rotation=45)

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.gcf().autofmt_xdate()

    plt.grid(True)
    plt.legend()
    plt.show()


# backtest the strategy. Portfolio starts with 1000 USD
# the df should have a column called 'signal' with 1 for buy and 0 for sell
def backtest(df):
    usd_balance = 1000
    btc_balance = 0
    eth_balance = 0
    portfolio = []

    for index, row in df.iterrows():
        if row['signal'] == 1:
            # buy 100 USD worth of BTC
            btc_balance += 100 / row['price_BTC']
            usd_balance -= 100
            # sell 100 USD worth of ETH
            eth_balance -= 100 / row['price_ETH']
            usd_balance += 100
        else:
            # buy 100 USD worth of ETH
            eth_balance += 100 / row['price_ETH']
            usd_balance -= 100
            # sell 100 USD worth of BTC
            btc_balance -= 100 / row['price_BTC']
            usd_balance += 100

        # calculate the total value of the portfolio
        total_value = usd_balance + btc_balance * row['price_BTC'] + eth_balance * row['price_ETH']
        portfolio.append([total_value, btc_balance, eth_balance, usd_balance])

    # create df for strategy results
    strategy_result_df = pd.DataFrame(portfolio, columns=['portfolio_value', 'btc_balance', 'eth_balance', 'usd_balance'])

    return strategy_result_df


strategy_result_df = backtest(combined_df)
print(strategy_result_df.head())