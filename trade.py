import pandas as pd

# Read the CSV file
file_path = './single.csv'
df = pd.read_csv(file_path)

# Calculate total traded values for all symbols including buy and sell values
df['total_buy_value'] = df.apply(lambda x: x['quantity'] * x['price'] if x['trade_type'] == 'buy' else 0, axis=1)
df['total_sell_value'] = df.apply(lambda x: x['quantity'] * x['price'] if x['trade_type'] == 'sell' else 0, axis=1)
total_values = df.groupby('symbol').agg({
    'total_buy_value': 'sum',
    'total_sell_value': 'sum'
}).reset_index()

# Calculate total profit as total_sell_value - total_buy_value
total_values['total_profit'] = total_values['total_sell_value'] - total_values['total_buy_value']

# Add traded_value column (total of buy and sell values)
total_values['traded_value'] = total_values['total_buy_value'] + total_values['total_sell_value']

# Sort by most traded to least traded symbol
sorted_traded_values = total_values.sort_values(by='traded_value', ascending=False)

# Prepare DataFrames for buy and sell trades
buys = df[df['trade_type'] == 'buy'].sort_values(['symbol', 'trade_date', 'order_execution_time'])
sells = df[df['trade_type'] == 'sell'].sort_values(['symbol', 'trade_date', 'order_execution_time'])

def calculate_profit(buys, sells):
    profit_data = []
    for symbol in buys['symbol'].unique():
        # print(f"Processing symbol: {symbol}")
        
        symbol_buys = buys[buys['symbol'] == symbol].copy()
        symbol_sells = sells[sells['symbol'] == symbol].copy()

        buy_index, sell_index = 0, 0
        while buy_index < len(symbol_buys) and sell_index < len(symbol_sells):
            buy_row = symbol_buys.iloc[buy_index]
            sell_row = symbol_sells.iloc[sell_index]
            
            # print(f"Buy row: {buy_row.to_dict()}")
            # print(f"Sell row: {sell_row.to_dict()}")

            if buy_row['quantity'] == sell_row['quantity']:
                profit = (sell_row['price'] - buy_row['price']) * buy_row['quantity']
                profit_data.append({
                    'symbol': symbol, 
                    'quantity': buy_row['quantity'], 
                    'profit': profit,
                    'buy_order_execution_time': buy_row['order_execution_time'],
                    'sell_order_execution_time': sell_row['order_execution_time']
                })
                # print(f"Matched equal quantity: {buy_row['quantity']} with profit: {profit}")
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
                symbol_sells.iloc[sell_index, symbol_sells.columns.get_loc('quantity')] -= buy_row['quantity']
                # print(f"Matched partial buy quantity: {buy_row['quantity']} with profit: {profit}")
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
                symbol_buys.iloc[buy_index, symbol_buys.columns.get_loc('quantity')] -= sell_row['quantity']
                # print(f"Matched partial sell quantity: {sell_row['quantity']} with profit: {profit}")
                sell_index += 1

    # print(f"Profit data: {profit_data}")
    return pd.DataFrame(profit_data)

profit_df = calculate_profit(buys, sells)

# Save results to a CSV file
output_file_path = 'output.csv'
profit_df.to_csv(output_file_path, index=False)

# Display results
print("Total Traded Values for all Symbols:")
print(sorted_traded_values)
print("\nProfit Data:")
print(profit_df)
