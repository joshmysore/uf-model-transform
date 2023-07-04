import pandas as pd
import numpy as np

# Step 1: Read the spreadsheet into a DataFrame
df = pd.read_excel('12-month-statement.xlsx')

# Initialize target_column to None
code_column = None

# Find the column that contains codes based on revenue code
for col in df.columns:
    if '40100-00' in df[col].values:
        code_column = col
        break

# Check if code_column is None (i.e., the codes were not found)
if code_column is None:
    print("Could not find revenue column.")
else:
    # The column to the right of the code column is the name column
    name_column = df.columns[df.columns.get_loc(code_column) + 1]

    # Filter rows based on the code ranges
    RE_rows = df[(df[code_column] >= '50010-00') & (df[code_column] <= '59999-99')]
    NRE_rows = df[(df[code_column] >= '61000-00') & (df[code_column] <= '69999-99')]

    # Initialize the dictionaries to hold the data
    RE_data = {(code, RE_rows.loc[RE_rows[code_column] == code, name_column].values[0].strip().title()): [] for code in RE_rows[code_column]}
    NRE_data = {(code, NRE_rows.loc[NRE_rows[code_column] == code, name_column].values[0].strip().title()): [] for code in NRE_rows[code_column]}

    # Iterate over the columns in the DataFrame
    for col in df.columns:
        # Try to convert the first cell in the column to a datetime
        try:
            date = pd.to_datetime(df[col][0], format='%b %Y', errors='coerce')
        except ValueError:
            # If the conversion failed, continue to the next column
            continue

        # If the conversion was successful, this column contains data for a specific date
        if pd.notnull(date):
            # Get the data for the RE and NRE codes
            for (code, name) in RE_data:
                RE_data[(code, name)].append(RE_rows.loc[RE_rows[code_column] == code, col].values[0])
            for (code, name) in NRE_data:
                NRE_data[(code, name)].append(NRE_rows.loc[NRE_rows[code_column] == code, col].values[0])

    # Print the RE and NRE data
    print("RE data:")
    for (code, name), data in RE_data.items():
        print(f"{code}: {name}")
    print("NRE data:")
    for (code, name), data in NRE_data.items():
        print(f"{code}: {name}")
