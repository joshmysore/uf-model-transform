import pandas as pd
import requests
from datetime import datetime
from alpha_vantage.foreignexchange import ForeignExchange
import openpyxl

# Step 1: Read the spreadsheet into a DataFrame
df = pd.read_excel('12-month-statement.xlsx')

code_column = None
code_prefixes = [(4, 'REV'), (5, 'RE'), (6, 'NRE'), (7, 'C&GE'), (8, 'OI&E'), (9, 'OI&E')]
groups = {i: {"codes": [], "names": [], "final": [], "prefix": prefix} for i, prefix in code_prefixes}

# Find the column that contains codes based on revenue code
for col in df.columns:
    if '40100-00' in df[col].values:
        code_column = col
        break

if code_column is None:
    print("Could not find revenue column.")
else:
    name_column = df.columns[df.columns.get_loc(code_column) + 1]

    # For each group, filter rows based on the code, create a dictionary and populate the lists
    for i, prefix in code_prefixes:
        group_rows = df[(df[code_column] >= f'{i}0000-00') & (df[code_column] <= f'{i}9999-99')]
        group_data = {(code, f"{prefix} - " + group_rows.loc[group_rows[code_column] == code, name_column].values[0].strip().title()): [] for code in group_rows[code_column]}
        
        for (code, name), data in group_data.items():
            groups[i]["codes"].append(code)
            groups[i]["names"].append(name)
            groups[i]["final"].append(code + ": " + name)

# All pre-read work
codes = [code for group in groups.values() for code in group["codes"]]
col_final = [final for group in groups.values() for final in group["final"]]
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

# Sort this list based on the entire code
column_tuples.sort(key=lambda x: int(x[1].split('-')[0] + x[1].split('-')[1]))

# Extract the sorted list of original column names
sorted_columns = [col[0] for col in column_tuples]

# Rearrange the columns in the dataframe
output_df = output_df[sorted_columns]

# create variable for column position of 0
new_position = 0

def fetch_exchange_rate(date):
    url = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=CLF&to_symbol=CLP&apikey=5TLIDN7TN6IQZJUE'
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

def create_and_format_column(df, new_col_name, codes, divisors=None, rounding=0, position=None, factor=1., subtract_codes=None):
    subtract_cols = []
    cols_to_sum = [col for col in df.columns if any(code in col for code in codes)]

    if subtract_codes is not None:
        subtract_cols = [col for col in df.columns if any(code in col for code in subtract_codes)]
        for col in subtract_cols:
            if col in cols_to_sum:  # check if column is in cols_to_sum before removing
                cols_to_sum.remove(col)  

    print(f'{new_col_name}: {cols_to_sum}')  # Debug line
    # print(f'Columns to be subtracted for {new_col_name}: {subtract_cols}')  # Debug line

    df[new_col_name] = df[cols_to_sum].sum(axis=1)
    df[new_col_name] -= df[subtract_cols].sum(axis=1)

    if divisors is not None:
        # print(f'Divisors for {new_col_name}: {divisors}')  # Debug line
        for i, divisor in enumerate(divisors):
            df.loc[df.index[i], new_col_name] = df.loc[df.index[i], new_col_name] / divisor

    if factor != 1.:
        df[new_col_name] *= factor

    if rounding is not None:
        df[new_col_name] = df[new_col_name].round(rounding)

    if position is not None:
        cols = df.columns.tolist()
        cols.insert(position, cols.pop(cols.index(new_col_name)))
        df = df.reindex(columns=cols)

    # print(f'Data for {new_col_name}: {df[new_col_name]}')  # Debug line

    return df

divisors = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Payroll',
    codes=['1110-10', # Cleaning-Payroll
           '1110-15', # Cleaning-Contract Service
           '2110-10', # R&M-Payroll-Salaries
           '2140-10', # R&M-Payroll-Outside Contract
           '5110-10', # Administrative-Payroll-Salaries
           '5120-10', # Administrative-Payroll-Reimbursed-Labor
           '5140-10', # Administrative-Payroll-Outside Contract
           '5330-10'], # Other Professional Fees
    divisors=divisors,
    position=new_position,
    factor=-1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Marketing',
    codes=['8220-10', # Advertising & Promo
           '8330-10'], # Marketing
    divisors=divisors,
    rounding=0,
    position=new_position + 1,
    factor=-1
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
           '4210-10', # Landscaping-Gardening Payroll
           '4210-20', # Landscaping-Gardening Contract
           '4230-20', # Pool-Service Contract
           '4245-10'],# Turn-Over--Painting
    divisors=divisors,
    position=new_position + 2,
    factor=-1
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
           '95200-15', # OI&E - Appraisal Fee (category 9)
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
    position=new_position + 3,
    factor=-1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Utilities',
    codes=['4110-10', # Electricity
           '4120-10', # Gas
           '4130-10'], # Water/Sewer
    divisors=divisors,
    position=new_position + 4,
    factor=-1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Others',
    codes=['1400-10', # Miscellaneous - Covid19
           '5050-30', # Non Creditable Vat
           '5060-10', # Late Fees
           '5610-10', # Travel - General
           '5630-10', # Auto Expense, Parking & Mileage
           '5630-11', # Non-Deductible Reimbursements
           '8260-10', # Tenant Activity/Relations
           '8290-10', # Tenant Subsidy
           '8230-11', # Meals & Enternainment from General Leasing Expense
           '70110-10', # C&GE - Legal Services (category 7)
           '93110-10'], # OI&E - Bank Charges (category 9)
    subtract_codes= ['91010-10', # OI&E - Interest Income-Investment (category 9) (negative in model)
                     '91050-10'], # OI&E - Interest Income-Others (category 9) (negative in model)
    divisors=divisors,
    position=new_position + 5,
    factor=-1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='OpEx - Property Management Fee',
    codes=['5215-10'], # Property Mgmnt Fee-3Rd Party
    divisors=divisors,
    position=new_position + 6,
    factor=-1
)

output_df['OpEx - Maintenance'] = output_df['OpEx - Payroll'] + output_df['OpEx - Marketing'] + output_df['OpEx - Repairs & Maintenance'] + output_df['OpEx - Office Expenses'] + output_df['OpEx - Utilities'] + output_df['OpEx - Others']
output_df.insert(new_position + 7, 'OpEx - Maintenance', output_df.pop('OpEx - Maintenance'))

output_df['OpEx - Total'] = output_df['OpEx - Maintenance'] + output_df['OpEx - Property Management Fee']
output_df.insert(new_position + 8, 'OpEx - Total', output_df.pop('OpEx - Total'))

output_df = create_and_format_column(
    df=output_df,
    new_col_name='SG&A - Real Estate Taxes',
    codes=['7110-10'], # Real Estate Taxes
    divisors=divisors,
    position=new_position + 9,
    factor=-1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='SG&A - Insurance',
    codes=['7230-10'], # Property Insurance
    divisors=divisors,
    position=new_position + 10,
    factor=-1
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='SG&A - Leasing Comissions',
    codes=[ # REVENUES W/O VAT
           '43310-10', # REV - Parking Operation Income (category 4, Residential Parking Income)
           '43330-10', # REV - Parking Base Rent (category 4, Residential Parking Income)
           '43350-10', # REV - Parking Concession (category 4, Residential Parking Income)
           '43021-01', # REV - Storage Income (category 4)
           '41310-10', # REV - Lease Cancelations (category 4, Other Income)
           '42051-10', # REV - Tenant Work Order (category 4, Other Income)
           '42480-10', # REV - Miscellaneous Income (category 4, Other Income)
           '42510-10', # REV - Key Income (category 4, Other Income)
           '42515-10', # REV - Application Fee (category 4, Other Income)
           '42560-10', # REV - Tenant Damage Income (category 4, Other Income)
           '43013-20', # REV - Pet Rent (category 4, Other Income)
           '43021-02', # REV - Facility Use Fee (category 4, Other Income)
           # REVENUES W/ VAT
           # Effective Service Revenues
           '42030-10', # REV - Cleaning Charges Income (category 4, Effective Service Revenues)
           # Effective Residential Revenues
           '41130-10', # REV - Rent - Residential (category 4, Residential Leasing)
           '41347-10', # REV - Gain/Loss To Lease (category 4, Gain/Loss To Lease)
           '41350-30', # REV - Rent Vacancy - Residential (category 4, Less: Vacancy Factor)
           '41320-10', # REV - Rent Concessions (category 4, Less: Concessions)
           '41347-20', # REV - Loss From Model (category 4, Less: Model Units)
           '5050-10'], # Bad Debt Expense (Less: Credit Losses)
    divisors=divisors,
    position=new_position + 11,
    factor=-0.025
)

output_df['SG&A - Total'] = output_df['SG&A - Real Estate Taxes'] + output_df['SG&A - Insurance'] + output_df['SG&A - Leasing Comissions']
output_df.insert(new_position + 12, 'SG&A - Total', output_df.pop('SG&A - Total'))

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Residential Leasing',
    codes=['41130-10'], # REV - Rent - Residential
    divisors=divisors,
    position=new_position + 13
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Gain/Loss To Lease',
    codes=['41347-10'], # REV - Gain/Loss To Lease
    divisors=divisors,
    position=new_position + 14
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Less: Vacancy Factor',
    codes=['41350-30'], # REV - Rent Vacancy
    divisors=divisors,
    position=new_position + 15
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Less: Concessions',
    codes=['41320-10'], # REV - Rent Concessions
    divisors=divisors,
    position=new_position + 16
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Less: Model Units',
    codes=['41347-20'], # REV - Loss From Model
    divisors=divisors,
    position=new_position + 17
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Less: Credit Losses',
    codes=['5050-10'], # Bad Debt Expense
    divisors=divisors,
    position=new_position + 18,
    factor = -1
)

output_df['Effective Residential Revenues'] = output_df['Revenues w/ VAT - Residential Leasing'] + output_df['Revenues w/ VAT - Gain/Loss To Lease'] + output_df['Revenues w/ VAT - Less: Vacancy Factor'] + output_df['Revenues w/ VAT - Less: Concessions'] + output_df['Revenues w/ VAT - Less: Model Units'] + output_df['Revenues w/ VAT - Less: Credit Losses']
output_df.insert(new_position + 19, 'Effective Residential Revenues', output_df.pop('Effective Residential Revenues'))

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/ VAT - Service Revenues',
    codes=['42030-10'], # REV - Cleaning Charges Income
    divisors=divisors,
    position=new_position + 20
)

output_df['Effective Service Revenues'] = output_df['Revenues w/ VAT - Service Revenues']
output_df.insert(new_position + 21, 'Effective Service Revenues', output_df.pop('Effective Service Revenues'))

output_df['Revenues w/ VAT'] = output_df['Effective Residential Revenues'] + output_df['Effective Service Revenues']
output_df.insert(new_position + 22, 'Revenues w/ VAT', output_df.pop('Revenues w/ VAT'))

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/o VAT - Residential Parking Income',
    codes=['43310-10', # REV - Parking Operation Income 
           '43330-10', # REV - Parking Base Rent
           '43350-10'], # REV - Parking Concession
    divisors=divisors,
    position=new_position + 23
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/o VAT - Storage Income',
    codes=['43021-01'], # REV - Storage Income
    divisors=divisors,
    position=new_position + 24
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/o VAT - Other Income',
    codes=['41310-10', # REV - Lease Cancelations 
           '42051-10', # REV - Tenant Work Order 
           '42480-10', # REV - Miscellaneous Income 
           '42510-10', # REV - Key Income
           '42515-10', # REV - Application Fee 
           '42560-10', # REV - Tenant Damage Income 
           '43013-20', # REV - Pet Rent 
           '43021-02'], # REV - Facility Use Fee
    divisors=divisors,
    position=new_position + 25
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/o VAT - Less: Vacancy Factor',
    codes=[],
    divisors=divisors,
    position=new_position + 26
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Revenues w/o VAT - Less: Credit Losses',
    codes=[],
    divisors=divisors,
    position=new_position + 27
)

output_df['Revenues w/o VAT'] = output_df['Revenues w/o VAT - Residential Parking Income'] + output_df['Revenues w/o VAT - Storage Income'] + output_df['Revenues w/o VAT - Other Income'] + output_df['Revenues w/o VAT - Less: Vacancy Factor'] + output_df['Revenues w/o VAT - Less: Credit Losses']
output_df.insert(new_position + 28, 'Revenues w/o VAT', output_df.pop('Revenues w/o VAT'))

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Maintenance - Maintenance Reimbursements',
    codes=['41410-20', # REV - Cam Recovery-Estimate
           '41130-20'], # REV - Rental - Additional Services
    divisors=divisors,
    position=new_position + 29
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Maintenance - Less: Vacancy Factor',
    codes=[],
    divisors=divisors,
    position=new_position + 30
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Maintenance - Less: Model Units',
    codes=[],
    divisors=divisors,
    position=new_position + 31
)

output_df = create_and_format_column(
    df=output_df,
    new_col_name='Maintenance - Less: Credits Losses',
    codes=[],
    divisors=divisors,
    position=new_position + 32
)

output_df['Maintenance'] = output_df['Maintenance - Maintenance Reimbursements'] + output_df['Maintenance - Less: Vacancy Factor'] + output_df['Maintenance - Less: Model Units'] + output_df['Maintenance - Less: Credits Losses']
output_df.insert(new_position + 33, 'Maintenance', output_df.pop('Maintenance'))

output_df['Total Revenue'] = output_df['Revenues w/ VAT'] + output_df['Revenues w/o VAT'] + output_df['Maintenance']
output_df.insert(new_position + 34, 'Total Revenue', output_df.pop('Total Revenue'))

# create a new column of the divisors next to OpEx - Payroll
output_df.insert(new_position, 'UF', divisors)

#output excel file transposing the rows and columns
output_df.T.to_excel('output.xlsx')