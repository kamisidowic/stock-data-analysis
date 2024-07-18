import pandas as pd

# Load the traded_data.csv file
traded_data_file_path = './traded_data.csv'
traded_data_df = pd.read_csv(traded_data_file_path)

# Load the unrealized_zero_output_cleaned.xlsx file
unrealized_zero_file_path = './unrealized_zero_output_cleaned.xlsx'
unrealized_zero_df = pd.read_excel(unrealized_zero_file_path)

# Merge the two DataFrames on the 'symbol' column
merged_df = pd.merge(traded_data_df, unrealized_zero_df, left_on='symbol', right_on='Symbol', how='inner')

# Select and rename the columns to match the requirements
comparison_df = merged_df[['symbol', 'total_buy_quantity', 'Quantity', 'total_buy_value', 'Buy Value', 'total_sell_value', 'Sell Value', 'total_profit', 'Realized P&L']]

# Save the comparison DataFrame to a new CSV file
# output_file_path = './matched_traded_data.csv'
# comparison_df.to_csv(output_file_path, index=False)

# Save the comparison DataFrame to a new Excel file
output_file_path = './matched_traded_data.xlsx'
comparison_df.to_excel(output_file_path, index=False)


# Display the results
print("Matched Data:")
print(comparison_df.head())
