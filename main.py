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

# create a column called OpEx - Payroll that does the following calculation: 
    # the sum of the following columns: 51110-10: RE - Cleaning-Payroll,
    #       61110-10: NRE - Cleaning-Payroll,
    #       51110-15: RE - Cleaning-Contract Service,
    #       61110-15: NRE - Cleaning-Contract Service,
    #       62110-10: NRE - R&M-Payroll-Salaries,
    #       62140-10: NRE - R&M-Payroll-Outside Contract,
    #       65110-10: NRE - Administrative-Payroll-Salaries,
    #       65140-10: NRE - Administrative-Payroll-Outside Contract,
    #       55330-10: RE - Other Professional Fees
    #       65330-10: NRE - Other Professional Fees) divided by 35,510 rounded to the nearest whole number
output_df['OpEx - Payroll'] = output_df['51110-10: RE - Cleaning-Payroll'] + output_df['61110-10: NRE - Cleaning-Payroll'] + output_df['51110-15: RE - Cleaning-Contract Service'] + output_df['61110-15: NRE - Cleaning-Contract Service'] + output_df['62110-10: NRE - R&M-Payroll-Salaries'] + output_df['62140-10: NRE - R&M-Payroll-Outside Contract'] + output_df['65110-10: NRE - Administrative-Payroll-Salaries'] + output_df['65140-10: NRE - Administrative-Payroll-Outside Contract'] + output_df['55330-10: RE - Other Professional Fees'] + output_df['65330-10: NRE - Other Professional Fees']
output_df['OpEx - Payroll'] = output_df['OpEx - Payroll'] / 35510 
output_df['OpEx - Payroll'] = output_df['OpEx - Payroll'].round(0)

# place the column OpEx - Maintenance in the first column position
cols = output_df.columns.tolist()
cols.insert(0, cols.pop(cols.index('OpEx - Payroll')))
output_df = output_df.reindex(columns=cols)

# output the dataframe to a new excel file
output_df.to_excel('output.xlsx')
