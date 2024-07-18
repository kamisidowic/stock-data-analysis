import pandas as pd

# Load the unrealized_zero_output_cleaned.xlsx file to get the list of symbols
unrealized_zero_file_path = './unrealized_zero_output_cleaned.xlsx'
unrealized_zero_df = pd.read_excel(unrealized_zero_file_path)
symbols = unrealized_zero_df['Symbol'].tolist()

# Load the file.csv file containing all the trade data
trade_data_file_path = './file.csv'
trade_df = pd.read_csv(trade_data_file_path)

# Split the trades into two DataFrames
trades_with_symbols = trade_df[trade_df['symbol'].isin(symbols)]
trades_without_symbols = trade_df[~trade_df['symbol'].isin(symbols)]

# Save these two DataFrames into separate CSV files
trades_with_symbols_file_path = './trades_with_symbols.csv'
trades_without_symbols_file_path = './trades_without_symbols.csv'
trades_with_symbols.to_csv(trades_with_symbols_file_path, index=False)
trades_without_symbols.to_csv(trades_without_symbols_file_path, index=False)

# Display the results
print("Trades with symbols in unrealized_zero_output_cleaned.xlsx:")
print(trades_with_symbols.head())

print("\nTrades without symbols in unrealized_zero_output_cleaned.xlsx:")
print(trades_without_symbols.head())
