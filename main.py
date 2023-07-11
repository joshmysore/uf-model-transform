import pandas as pd
import requests
from datetime import datetime
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

# create variable for column position of 0
new_position = 0

def fetch_exchange_rate(date):
    url = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=CLF&to_symbol=CLP&apikey=YOUR_API_KEY'
    r = requests.get(url)
    data = r.json()

    # Extract the monthly exchange rate data from the response
    monthly_rates = data['Time Series FX (Monthly)']

    # List to store the exchange rates
    exchange_rates = []

    # Iterate over the monthly data and extract the exchange rates
    for date, rate in monthly_rates.items():
        # Convert the date string to a datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        # Format the date as "Month Year" (e.g., "Jun 2022")
        month_year = date_obj.strftime('%b %Y')

        # Check if the month/year is in the dates list
        if month_year in dates:
            exchange_rate = rate['4. close']
            exchange_rates.append((month_year, exchange_rate))

    # Sort the exchange rates based on the month/year in ascending order
    exchange_rates.sort(key=lambda x: datetime.strptime(x[0], '%b %Y'))

    # Extract the exchange rates from the list of tuples
    divisors_UF = [x[1] for x in exchange_rates]

    # Convert the exchange rates to floats
    divisors_UF = [float(x) for x in divisors_UF]

    return divisors_UF

def create_and_format_column(df, new_col_name, codes, divisors=None, rounding=0, position=None):
    cols_to_sum = [col for col in df.columns if any(code in col for code in codes)]

    # print(f'Columns to be summed for {new_col_name}: {cols_to_sum}')  # Debug line

    df[new_col_name] = df[cols_to_sum].sum(axis=1)

    if divisors is not None:
        # print(f'Divisors for {new_col_name}: {divisors}')  # Debug line
        for i, divisor in enumerate(divisors):
            df.loc[df.index[i], new_col_name] = df.loc[df.index[i], new_col_name] / divisor

    if rounding is not None:
        df[new_col_name] = df[new_col_name].round(rounding)

    if position is not None:
        cols = df.columns.tolist()
        cols.insert(position, cols.pop(cols.index(new_col_name)))
        df = df.reindex(columns=cols)

    # print(f'Data for {new_col_name}: {df[new_col_name]}')  # Debug line

    return df

divisors = fetch_exchange_rate(dates)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Payroll',
    codes=['1110-10', # Cleaning-Payroll
           '1110-15', # Cleaning-Contract Service
           '2110-10', # R&M-Payroll-Salaries
           '2140-10', # R&M-Payroll-Outside Contract
           '5110-10', # Administrative-Payroll-Salaries
           # Missing Administrative-Payroll-Reimbursed-Labor
           '5140-10', # Administrative-Payroll-Outside Contract
           '5330-10'], # Other Professional Fees
    divisors=divisors,
    position=new_position
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Marketing',
    codes=['8220-10', # Advertising & Promo
           '8330-10'], # Marketing
    divisors=divisors,
    rounding=0,
    position=new_position + 1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Repairs & Maintenance',
    codes=['2210-20', # Elevator/Escalator-Service Contracts
           '2610-40', # Plumbing-Repairs & Maintenance
           '2710-20', # Fire & Safety-R&M Contract
           '2710-40', # Fire & Safety-Repairs & Maintenance
           '2710-50', # Fire & Safety-Supplies & Materials
           '3990-20', # Repairs And Maintenance
           '2810-20', # Pest Control-Contract
           '4210-10', # Landscaping-Gardening Payroll (guess at code)
           '4210-20', # Landscaping-Gardening Contract
           '4230-20', # Pool-Service Contract
           '4245-10'],# Turn-Over--Painting
    divisors=divisors,
    position=new_position + 2
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Office Expenses',
    codes=['1110-40', # Cleaning-Repairs&Maintenance
           '1110-50', # Cleaning-Supplies&Materials
           '3120-10', # Bldg R&M (Interior)-Lock & Keys
           '3160-10', # Bldg R&M (Interior)-Supplies & Materials
           '3165-10', # Bldg R&M (Interior)-Uniforms
           '3180-30', # Bldg R&M (Interior)-Generator
           '4140-10', # Telephone
           '4820-10', # Supplies & Materials
           '5310-10', # Accounting/Tax
           # missing Appraisal Fee
           '5320-10', # Legal Fees
           '5330-10', # Other Professional Fees
           '5405-10', # Meals & Entertainment
           '5410-20', # Office Employee Parking
           '5420-10', # Office Furniture/Equipment Rental
           '5430-10', # Office Supplies
           '5440-10', # Office Expense
           '5440-95', # Telecom/Internet
           '5465-10', # Credit Card Fee
           '5470-10', # License, Permit, & Fees
           '5480-10', # Postage/Messengerial
           '5550-10'], # Training & Seminar
    divisors=divisors,
    rounding=0,
    position=new_position + 3
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Utilities',
    codes=['4110-10', # Electricity
           '4120-10', # Gas
           '4130-10'], # Water/Sewer
    divisors=divisors,
    position=new_position + 4
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Others',
    codes=['1400-10', #  Miscellaneous - Covid19
           '5050-30', # Non Creditable Vat
           '5060-10', # Late Fees
           '5610-10', # Travel - General
           '5630-10', # Auto Expense, Parking & Mileage
           '5630-11', # Non-Deductible Reimbursements
           '8260-10', # Tenant Activity/Relations
           '8290-10' # Tenet Subsidy
           # Missing Meals & Enternainment from General Leasing Expense
           # Missing Legal Service from Other Expenses
           # Missing Interest Income-Investment from Other Expenses
           # Missing Bank Charges from Other Expenses
           ], 
    divisors=divisors,
    position=new_position + 5
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Property Management Fee',
    codes=['5215-10'], # Property Mgmnt Fee-3Rd Party
    divisors=divisors,
    position=new_position + 6
)

output_df['OpEx - Maintenance'] = output_df['OpEx - Payroll'] + output_df['OpEx - Marketing'] + output_df['OpEx - Repairs & Maintenance'] + output_df['OpEx - Office Expenses'] + output_df['OpEx - Utilities'] + output_df['OpEx - Others']
output_df.insert(new_position, 'OpEx - Maintenance', output_df.pop('OpEx - Maintenance'))

output_df['OpEx - Total'] = output_df['OpEx - Maintenance'] + output_df['OpEx - Property Management Fee']
output_df.insert(new_position + 7, 'OpEx - Total', output_df.pop('OpEx - Total'))

output_df = create_and_format_column(
    df=output_df,
    new_col_name='SG&A - Real Estate Taxes',
    codes=['7110-10'], # Real Estate Taxes
    divisors=divisors,
    position=new_position + 8
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='SG&A - Insurance',
    codes=['7230-10'], # Property Insurance
    divisors=divisors,
    position=new_position + 9
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='SG&A - Leasing Comissions',
    codes=[], 
    divisors=divisors,
    position=new_position + 10
)

output_df['SG&A - Total'] = output_df['SG&A - Real Estate Taxes'] + output_df['SG&A - Insurance'] + output_df['SG&A - Leasing Comissions']
output_df.insert(new_position + 11, 'SG&A - Total', output_df.pop('SG&A - Total'))

# create a new column of the divisors next to OpEx - Payroll
output_df.insert(new_position, 'UF', divisors)

#output excel file
output_df.to_excel('output.xlsx')