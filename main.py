import pandas as pd
import openpyxl

# Step 1: Read the spreadsheet into a DataFrame
df = pd.read_excel('12-month-statement.xlsx')

code_column = None
RE_codes = []
NRE_codes = []
RE_names = []
NRE_names = []
RE_final = []
NRE_final = []

# Find the column that contains codes based on revenue code
for col in df.columns:
    if '40100-00' in df[col].values:
        code_column = col
        break

if code_column is None:
    print("Could not find revenue column.")
else:
    name_column = df.columns[df.columns.get_loc(code_column) + 1]
    RE_rows = df[(df[code_column] >= '50010-00') & (df[code_column] <= '59999-99')]
    NRE_rows = df[(df[code_column] >= '61000-00') & (df[code_column] <= '69999-99')]
    RE_data = {(code, "RE - " + RE_rows.loc[RE_rows[code_column] == code, name_column].values[0].strip().title()): [] for code in RE_rows[code_column]}
    NRE_data = {(code, "NRE - " + NRE_rows.loc[NRE_rows[code_column] == code, name_column].values[0].strip().title()): [] for code in NRE_rows[code_column]}

    for (code, name), data in RE_data.items():
        RE_codes.append(code)
        RE_names.append(name)
        RE_final.append(code + ": " + name)

    for (code, name), data in NRE_data.items():
        NRE_codes.append(code)
        NRE_names.append(name)
        NRE_final.append(code + ": " + name)

# All pre-read work
codes = RE_codes + NRE_codes
col_final = RE_final + NRE_final
dates = []
data_dict = {}

# Iterate over each column
for col in df.columns:
    # Iterate over each row in the column
    for cell in df[col]:
        try:
            # Try to convert the cell to a datetime
            date = pd.to_datetime(cell, format='%b %Y', errors='coerce')

            # If the cell is a date
            if pd.notnull(date):
                date_str = cell
                dates.append(date_str)
                data_dict[date_str] = {}

                for code in codes:
                    # Get the row where the code matches in the original DataFrame
                    row = df[df[code_column] == code]

                    # If there's any matching row, get the corresponding value from the row with code
                    if not row.empty:
                        value = row.iat[0, df.columns.get_loc(col)]
                        data_dict[date_str][code] = value

                # Exit inner loop once the first date is found in the column
                break
        except ValueError:
            # If the cell couldn't be converted to a date, continue to the next cell
            continue

# Create a DataFrame with the collected dates as rows and the columns from codes
output_df = pd.DataFrame(data_dict).T

# Rename the columns with the final column names
output_df.columns = col_final

# delete all columns that do not have only have a header and then no data
output_df = output_df.dropna(axis=1, how='all')

print(output_df)