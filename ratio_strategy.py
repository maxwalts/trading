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

# add a column for the moving average
# combined_df['MA_long'] = combined_df['BTC.ETH'].rolling(48).mean()

# plot the ratio
plt.figure(figsize=(12, 6))
plt.plot(combined_df['timestamp'], combined_df['BTC.ETH'])
plt.xlabel('Timestamp')
plt.ylabel('BTC/ETH Price Ratio')
plt.title(f'Hourly BTC.ETH for the Last 90 Days with 24 Day Moving Average')
plt.xticks(rotation=45)

# add a line for the moving average
plt.plot(combined_df['timestamp'], combined_df['MA_short'], color='red')
# plt.plot(combined_df['timestamp'], combined_df['MA_long'], color='green')

date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
plt.gca().xaxis.set_major_formatter(date_formatter)
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.gcf().autofmt_xdate()

plt.grid(True)
plt.show()
