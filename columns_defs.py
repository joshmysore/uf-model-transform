column_definitions = [
{
    'new_col_name': 'UF',
    'divisor': True 
},
{
    'new_col_name': 'OpEx - Payroll',
    'codes': ['1110-10', # Cleaning-Payroll
                '1110-15', # Cleaning-Contract Service
                '2110-10', # R&M-Payroll-Salaries
                '2140-10', # R&M-Payroll-Outside Contract
                '5110-10', # Administrative-Payroll-Salaries
                '5120-10', # Administrative-Payroll-Reimbursed-Labor
                '5140-10', # Administrative-Payroll-Outside Contract
                '5330-10'], # Other Professional Fees
    'factor': -1
},
{
    'new_col_name': 'OpEx - Marketing',
    'codes': ['8220-10', '8330-10'],
    'factor': -1
},
{
    'new_col_name': 'OpEx - Repairs & Maintenance',
    'codes': ['2210-20', '2610-40', '2710-20', '2710-40', '2710-50', '3990-20', '2810-20', '4210-10', '4210-20', '4230-20', '4245-10'],
    'factor': -1
},
{
    'new_col_name': 'OpEx - Office Expenses',
    'codes': ['1110-40', '1110-50', '3120-10', '3160-10', '3165-10', '3180-30', '4140-10', '4820-10', '5310-10', '95200-15', '5320-10', '5330-10', '5405-10', '5410-20', '5420-10', '5430-10', '5440-10', '5440-95', '5465-10', '5470-10', '5480-10', '5550-10'],
    'factor': -1
},
{
    'new_col_name': 'OpEx - Utilities',
    'codes': ['4110-10', '4120-10', '4130-10'],
    'factor': -1
},
{
    'new_col_name': 'OpEx - Others',
    'codes': ['1400-10', '5050-30', '5060-10', '5610-10', '5630-10', '5630-11', '8260-10', '8290-10', '8230-11', '70110-10', '93110-10'],
    'subtract_codes': ['91010-10', '91050-10'],
    'factor': -1
},
{
    'new_col_name': 'OpEx - Property Management Fee',
    'codes': ['5215-10'],
    'factor': -1
},
{
    'new_col_name': 'OpEx - Maintenance',
    'sum_columns': ['OpEx - Marketing', 'OpEx - Repairs & Maintenance', 'OpEx - Office Expenses', 'OpEx - Utilities', 'OpEx - Others']
},
{
    'new_col_name': 'OpEx - Total',
    'sum_columns': ['OpEx - Maintenance', 'OpEx - Property Management Fee']
},
{
    'new_col_name': 'SG&A - Real Estate Taxes',
    'codes': ['7110-10'],
    'factor': -1
},
{
    'new_col_name': 'SG&A - Insurance',
    'codes': ['7230-10'],
    'factor': -1
},
{
    'new_col_name': 'SG&A - Leasing Comissions',
    'codes': ['43310-10', '43330-10', '43350-10', '43021-01', '41310-10', '42051-10', '42480-10', '42510-10', '42515-10', '42560-10', '43013-20', '43021-02', '42030-10', '41130-10', '41347-10', '41350-30', '41320-10', '41347-20', '5050-10'],
    'factor': -0.025
},
{
    'new_col_name': 'SG&A - Total',
    'sum_columns': ['SG&A - Real Estate Taxes', 'SG&A - Insurance', 'SG&A - Leasing Comissions']
},
{
    'new_col_name': 'Revenues w/ VAT - Residential Leasing',
    'codes': ['41130-10']
},
{
    'new_col_name': 'Revenues w/ VAT - Gain/Loss To Lease',
    'codes': ['41347-10']
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Vacancy Factor',
    'codes': ['41350-30']
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Concessions',
    'codes': ['41320-10']
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Model Units',
    'codes': ['41347-20']
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Credit Losses',
    'codes': ['5050-10'],
    'factor': -1
},
{
    'new_col_name': 'Effective Residential Revenues',
    'sum_columns': ['Revenues w/ VAT - Residential Leasing', 'Revenues w/ VAT - Gain/Loss To Lease', 'Revenues w/ VAT - Less: Vacancy Factor', 'Revenues w/ VAT - Less: Concessions', 'Revenues w/ VAT - Less: Model Units', 'Revenues w/ VAT - Less: Credit Losses']
},
{
    'new_col_name': 'Revenues w/ VAT - Service Revenues',
    'codes': ['42030-10']
},
{
    'new_col_name': 'Effective Service Revenues',
    'sum_columns': ['Revenues w/ VAT - Service Revenues']
},
{
    'new_col_name': 'Revenues w/ VAT',
    'sum_columns': ['Effective Residential Revenues', 'Effective Service Revenues']
},
{
    'new_col_name': 'Revenues w/o VAT - Residential Parking Income',
    'codes': ['43310-10', '43330-10', '43350-10']
},
{
    'new_col_name': 'Revenues w/o VAT - Storage Income',
    'codes': ['43021-01']
},
{
    'new_col_name': 'Revenues w/o VAT - Other Income',
    'codes': ['41310-10', '42051-10', '42480-10', '42510-10', '42515-10', '42560-10', '43013-20', '43021-02']
},
{
    'new_col_name': 'Revenues w/o VAT - Less: Vacancy Factor',
    'codes': []
},
{
    'new_col_name': 'Revenues w/o VAT - Less: Credit Losses',
    'codes': []
},
{
    'new_col_name': 'Revenues w/o VAT',
    'sum_columns': ['Revenues w/o VAT - Residential Parking Income', 'Revenues w/o VAT - Storage Income', 'Revenues w/o VAT - Other Income', 'Revenues w/o VAT - Less: Vacancy Factor', 'Revenues w/o VAT - Less: Credit Losses']
},
{
    'new_col_name': 'Maintenance - Maintenance Reimbursements',
    'codes': ['41410-20', '41130-20']
},
{
    'new_col_name': 'Maintenance - Less: Vacancy Factor',
    'codes': []
},
{
    'new_col_name': 'Maintenance - Less: Model Units',
    'codes': []
},
{
    'new_col_name': 'Maintenance - Less: Credits Losses',
    'codes': []
},
{
    'new_col_name': 'Maintenance',
    'sum_columns': ['Maintenance - Maintenance Reimbursements', 'Maintenance - Less: Vacancy Factor', 'Maintenance - Less: Model Units', 'Maintenance - Less: Credits Losses']
},
{
    'new_col_name': 'Total Revenue',
    'sum_columns': ['Revenues w/ VAT', 'Revenues w/o VAT', 'Maintenance']
}
]