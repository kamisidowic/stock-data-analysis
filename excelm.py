import pandas as pd

# Load the Excel file
file_path = './input/excelf.xlsx'
df = pd.read_excel(file_path)

# Filter rows where Unrealized P&L is 0
unrealized_zero_df = df[df['Unrealized P&L'] == 0]

# Drop the unnecessary columns
unrealized_zero_df = unrealized_zero_df.drop(columns=['Unnamed: 0', 'ISIN', 'Unrealized P&L'])

# Save the filtered and cleaned rows to a new Excel file
output_file_path = './output/unrealized_zero_output_cleaned.xlsx'
unrealized_zero_df.to_excel(output_file_path, index=False)

# Display the filtered and cleaned rows
# print("Filtered and cleaned rows where Unrealized P&L is 0:")
# print(unrealized_zero_df)
