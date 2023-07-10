import re
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

# Rename the columns to the final names
output_df.columns = col_final

# delete all columns that do not have only have a header and then no data
output_df = output_df.dropna(axis=1, how='all')

# delete all columns with the word "total" in the name
output_df = output_df[output_df.columns.drop(list(output_df.filter(regex='Total')))]

# Create a list of tuples where each tuple is (original_column_name, code)
column_tuples = [(col, col.split(':')[0]) for col in output_df.columns.tolist()]

# Sort this list based on the code (while ignoring the first digit)
column_tuples.sort(key=lambda x: int(x[1].split('-')[0][1:] + x[1].split('-')[1]))

# Extract the sorted list of original column names
sorted_columns = [col[0] for col in column_tuples]

# Rearrange the columns in the dataframe
output_df = output_df[sorted_columns]

def create_and_format_column(df, new_col_name, codes, divisors=None, rounding=None, position=None):
    cols_to_sum = [col for col in df.columns if any(code in col for code in codes)]

    df[new_col_name] = df[cols_to_sum].sum(axis=1)

    if divisors is not None:
        for i, divisor in enumerate(divisors):
            df.loc[df.index[i], new_col_name] = df.loc[df.index[i], new_col_name] / divisor

    if rounding is not None:
        df[new_col_name] = df[new_col_name].round(rounding)

    if position is not None:
        cols = df.columns.tolist()
        cols.insert(position, cols.pop(cols.index(new_col_name)))
        df = df.reindex(columns=cols)

    return df

# create variable for column position of 0
new_position = 0

# create list of divisors
divisors = [33087, 33417, 33837, 34258, 34600, 34812, 35111, 35288, 35510, 35575, 35839, 36033]

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Payroll',
    codes=['1110-10',
           '1110-15',
           '2110-10',
           '2140-10',
           '5110-10',
           '5140-10',
           '5330-10'],
    divisors=divisors,
    rounding=0,
    position=new_position
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Marketing',
    codes=['8220-10',
           '8330-10'],
    divisors=divisors,
    rounding=0,
    position=new_position + 1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Repairs & Maintenance',
    codes=['2210-20',
           '2610-40',
           '2710-20',
           '2710-20',
           '2710-40',
           '2710-50',
           '3990-20',
           '2810-20',
           '2810-20',
           '4210-10',
           '4210-20',
           '4230-20',
           '4245-10'],
    divisors=divisors,
    rounding=0,
    position=new_position + 2
)

#output excel file
output_df.to_excel('output.xlsx')