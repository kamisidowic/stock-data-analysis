import pandas as pd

# Read the CSV file
file_path = './trades_with_symbols.csv'
df = pd.read_csv(file_path)

# Convert order_execution_time to datetime
df['order_execution_time'] = pd.to_datetime(df['order_execution_time'])

# Calculate total traded values for all symbols
df['traded_value'] = df['quantity'] * df['price']

# Calculate total buy and sell values
df['total_buy_value'] = df.apply(lambda x: x['quantity'] * x['price'] if x['trade_type'] == 'buy' else 0, axis=1)
df['total_sell_value'] = df.apply(lambda x: x['quantity'] * x['price'] if x['trade_type'] == 'sell' else 0, axis=1)

# Calculate total buy 
# 'quantity': 'sum', returns buy + sell volume
df['total_buy_quantity'] = df.apply(lambda x: x['quantity'] if x['trade_type'] == 'buy' else 0, axis=1)

# Group by symbol and aggregate values
total_values = df.groupby('symbol').agg({
    'traded_value': 'sum',
    'total_buy_quantity': 'sum',
    'total_buy_value': 'sum',
    'total_sell_value': 'sum'
}).reset_index()

# Calculate total profit as total_sell_value - total_buy_value
total_values['total_profit'] = total_values['total_sell_value'] - total_values['total_buy_value']

# Sort by most traded to least traded symbol
sorted_traded_values = total_values.sort_values(by='symbol', ascending=True)

# Prepare DataFrames for buy and sell trades
buys = df[df['trade_type'] == 'buy'].sort_values(['symbol', 'order_execution_time'])
sells = df[df['trade_type'] == 'sell'].sort_values(['symbol', 'order_execution_time'])

def calculate_profit(buys, sells):
    profit_data = []
    for symbol in buys['symbol'].unique():
        symbol_buys = buys[buys['symbol'] == symbol].copy()
        symbol_sells = sells[sells['symbol'] == symbol].copy()

        buy_index, sell_index = 0, 0
        while buy_index < len(symbol_buys) and sell_index < len(symbol_sells):
            buy_row = symbol_buys.iloc[buy_index]
            sell_row = symbol_sells.iloc[sell_index]

            if buy_row['quantity'] == sell_row['quantity']:
                profit = (sell_row['price'] - buy_row['price']) * buy_row['quantity']
                profit_data.append({
                    'symbol': symbol,
                    'quantity': buy_row['quantity'],
                    'profit': profit,
                    'buy_order_execution_time': buy_row['order_execution_time'],
                    'sell_order_execution_time': sell_row['order_execution_time']
                })
                buy_index += 1
                sell_index += 1
            elif buy_row['quantity'] < sell_row['quantity']:
                profit = (sell_row['price'] - buy_row['price']) * buy_row['quantity']
                profit_data.append({
                    'symbol': symbol,
                    'quantity': buy_row['quantity'],
                    'profit': profit,
                    'buy_order_execution_time': buy_row['order_execution_time'],
                    'sell_order_execution_time': sell_row['order_execution_time']
                })
                symbol_sells.loc[sell_row.name, 'quantity'] -= buy_row['quantity']
                buy_index += 1
            else:
                profit = (sell_row['price'] - buy_row['price']) * sell_row['quantity']
                profit_data.append({
                    'symbol': symbol,
                    'quantity': sell_row['quantity'],
                    'profit': profit,
                    'buy_order_execution_time': buy_row['order_execution_time'],
                    'sell_order_execution_time': sell_row['order_execution_time']
                })
                symbol_buys.loc[buy_row.name, 'quantity'] -= sell_row['quantity']
                sell_index += 1

            # print(f"Processed: Symbol={symbol}, BuyIndex={buy_index}, SellIndex={sell_index}, BuyExecutionTime={buy_row['order_execution_time']}, SellExecutionTime={sell_row['order_execution_time']}")

    return pd.DataFrame(profit_data)

# Calculate initial profits
initial_profit_df = calculate_profit(buys, sells)

# Merge trades with the same buy_order_execution_time
merged_profit_data = initial_profit_df.groupby(['symbol', 'buy_order_execution_time']).apply(
    lambda x: pd.Series({
        'avg_buy_price': (x['quantity'] * x['buy_order_execution_time'].apply(lambda time: buys[buys['order_execution_time'] == time]['price'].mean())).sum() / x['quantity'].sum(),
        'quantity': x['quantity'].sum(),
        'avg_sell_price': (x['quantity'] * x['sell_order_execution_time'].apply(lambda time: sells[sells['order_execution_time'] == time]['price'].mean())).sum() / x['quantity'].sum(),
        'sell_order_execution_time': x['sell_order_execution_time'].iloc[-1],
        'profit': x['profit'].sum()
    })
).reset_index()

# Calculate holding days
merged_profit_data['holding_days'] = (pd.to_datetime(merged_profit_data['sell_order_execution_time']) - pd.to_datetime(merged_profit_data['buy_order_execution_time'])).apply(lambda x: f"{x.days} days, {x.seconds // 3600} hours")

# Save results to a CSV adn Excel

# Total traded data
traded_file_path_excel = 'traded_data.xlsx'
sorted_traded_values.to_excel(traded_file_path_excel, index=False)

traded_file_path_csv = 'traded_data.csv'
sorted_traded_values.to_csv(traded_file_path_csv, index=False)

# Profit data
output_file_path_excel = 'realisedop.xlsx'
merged_profit_data.to_excel(output_file_path_excel, index=False)

output_file_path_csv = 'realisedop.csv'
merged_profit_data.to_csv(output_file_path_csv, index=False)




# Display results
print("Total Traded Values for all Symbols:")
print(sorted_traded_values)
print("\nProfit Data:")
print(merged_profit_data)
