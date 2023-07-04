import pandas as pd
import numpy as np

# The dictionary holding the codes as keys and the corresponding column names as values
codes_and_columns = {
    '51110-10': 'RE - Cleaning: Payroll',
    '51110-15': 'RE - Cleaning: Contract Service',
    '51110-40': 'RE - Cleaning: Repairs & Maintenance',
    '51110-50': 'RE - Cleaning-Supplies & Materials',
    '61110-50': 'NRE - Cleaning-Supplies & Materials'  # Add more codes and column names as needed
}

# Step 1: Read the spreadsheet into a DataFrame
df = pd.read_excel('12-month-statement.xlsx')

dates = []
NRE_data = []
RE_data = []

# Initialize target_column to None
code_column = None

# Find the column that contains codes based on revenue code
for col in df.columns:
    if '40100-00' in df[col].values:
        code_column = col
        break

# Check if target_column is still None (i.e., the codes were not found)
if code_column is None:
    print("Could not find revenue column.")
else:
    # Find the rows with the codes "51110-50" and "61110-50"
    RE_clean_supplies = df[df[code_column] == '51110-50']
    NRE_clean_supplies = df[df[code_column] == '61110-50']

    # Check the number of rows found
    if NRE_clean_supplies.empty or RE_clean_supplies.empty:
        print("Could not find the rows with '51110-50' and/or '61110-50'.")
    else:
        # Iterate over each column
        for col in df.columns:
            # Iterate over each row in the column
            for i, cell in enumerate(df[col]):
                try:
                    # Try to convert the cell to a datetime
                    date = pd.to_datetime(cell, format='%b %Y', errors='coerce')

                    # If the conversion was successful (i.e., the cell was a date),
                    # store the original string and break the loop to move to the next column
                    if pd.notnull(date):
                        dates.append(cell)

                        # Store the data in the corresponding rows
                        NRE_data.append(NRE_clean_supplies.iat[0, df.columns.get_loc(col)])
                        RE_data.append(RE_clean_supplies.iat[0, df.columns.get_loc(col)])
                        break
                except ValueError:
                    # If the cell couldn't be converted to a date, continue to the next cell
                    continue

# Convert the lists to numpy arrays for element-wise addition
NRE_data_np = np.array(NRE_data)
RE_data_np = np.array(RE_data)

# Create a DataFrame with the collected data
output_df = pd.DataFrame({
    'Date': dates,
    'NRE - Cleaning-Supplies & Materials': NRE_data,
    'RE - Cleaning-Supplies & Materials': RE_data,
    'Total': NRE_data_np + RE_data_np  # element-wise addition
})

# Print the output DataFrame
print(output_df)

