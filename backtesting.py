import pandas as pd
import numpy as np
import btc_eth_ratio


# Define your trading strategy
# def trading_strategy(price_data):
#     # Implement your trading strategy here
#     # The function should return a Pandas DataFrame with buy/sell signals and trade sizes
#     # The DataFrame should have columns 'timestamp', 'buy_signal', 'sell_signal', 'buy_size', 'sell_size'
#     return strategy_data


# Define the moving average crossover strategy
# TODO: potential source of bias: is the daily price the average of the whole day, which we don't know until the end of the day?
def moving_average_crossover_strategy(price_data, short_window=10, long_window=20):
    # display the price data
    # print(price_data)
    # create close price column
    price_data['close'] = price_data['price']

    # Calculate the short-term and long-term moving averages
    price_data['short_moving_avg'] = price_data['close'].rolling(window=short_window).mean()
    price_data['long_moving_avg'] = price_data['close'].rolling(window=long_window).mean()

    # Generate buy and sell signals based on the moving average crossover
    price_data['buy_signal'] = np.where(price_data['short_moving_avg'] > price_data['long_moving_avg'], True, False)
    price_data['sell_signal'] = np.where(price_data['short_moving_avg'] < price_data['long_moving_avg'], True, False)

    # Calculate the buy and sell sizes based on available capital
    price_data['buy_size'] = np.where(price_data['buy_signal'], 1000 / price_data['close'], 0)
    price_data['sell_size'] = np.where(price_data['sell_signal'], 1000 / price_data['close'], 0)

    # Remove rows with missing data
    price_data = price_data.dropna()

    # Return the strategy data
    price_strategy_df = price_data[['timestamp', 'buy_signal', 'sell_signal', 'buy_size', 'sell_size']]
    price_strategy_df = price_strategy_df.dropna()
    
    return price_strategy_df


# Simulate trades based on your trading strategy
def simulate_trades(price_strategy_df):
    # Merge the price data with the strategy data
    # drop rows of price_data that have nan in long_moving_avg column
    price_strategy_df = price_strategy_df.dropna()
    # merged_data = pd.merge(price_data, strategy_data, on='timestamp', how='left')

    # Initialize variables for tracking trades and portfolio value
    portfolio_value = 0
    btc_balance = 0
    usd_balance = 1000  # replace with your own starting balance
    trades = []

    # Loop over each row in the merged data and simulate trades
    for i, row in price_strategy_df.iterrows():
        # If there is a buy signal, use the available USD balance to buy BTC
        if row['buy_signal']:
            btc_balance += row['buy_size']
            usd_balance -= row['close'] * row['buy_size']
            trades.append(('buy', row['close'], row['buy_size'], row['timestamp']))

        # If there is a sell signal, sell all BTC in the portfolio
        if row['sell_signal']:
            usd_balance += row['close'] * btc_balance
            trades.append(('sell', row['close'], btc_balance, row['timestamp']))
            btc_balance = 0

        # Calculate the portfolio value based on the current balances and BTC price
        portfolio_value = usd_balance + (btc_balance * row['close'])

    # Print the final portfolio value
    print(f'Final portfolio value: {portfolio_value}')
    print(f'Total number of trades: {len(trades)}')

    # Return the list of trades
    return trades


# Run the backtest
# get hourly data
price_data = btc_eth_ratio.get_hourly_prices('bitcoin', 90)
price_data = btc_eth_ratio.process_data(price_data)
price_strategy_df = moving_average_crossover_strategy(price_data)
trades = simulate_trades(price_strategy_df)


# Print the list of trades
# for trade in trades:
#     print(trade)
