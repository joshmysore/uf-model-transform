column_definitions = [
{
    'new_col_name': 'UF',
    'divisor': True 
},
{
    'new_col_name': 'Revenues w/ VAT - Residential Leasing',
    'codes': ['41130-10'], # REV - Rent - Residential
},
{
    'new_col_name': 'Revenues w/ VAT - Gain/Loss To Lease',
    'codes': ['41347-10'], # REV - Gain/Loss To Lease
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Vacancy Factor',
    'codes': ['41350-30'], # REV - Rent Vacancy - Residential
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Concessions',
    'codes': ['41320-10'], # REV - Rent Concessions
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Model Units',
    'codes': ['41347-20'], # REV - Loss From Model
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Credit Losses',
    'codes': ['65050-10'], # Bad Debt Expense
    'factor': -1
},
{
    'new_col_name': 'Effective Residential Revenues',
    'sum_columns': ['Revenues w/ VAT - Residential Leasing', 'Revenues w/ VAT - Gain/Loss To Lease', 'Revenues w/ VAT - Less: Vacancy Factor', 'Revenues w/ VAT - Less: Concessions', 'Revenues w/ VAT - Less: Model Units', 'Revenues w/ VAT - Less: Credit Losses']
},
{
    'new_col_name': 'Revenues w/ VAT - Service Revenues',
    'codes': ['42030-10'], # REV - Cleaning Charges Income
},
{
    'new_col_name': 'Revenues w/ VAT - Less: Vacancy Factor, Service Revenues',
    'codes': [], 
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
    'codes': ['43310-10', # REV - Parking Operation Income 
              '43330-10', # REV - Parking Base Rent
              '43350-10'], # REV - Parking Concession
},
{
    'new_col_name': 'Revenues w/o VAT - Storage Income',
    'codes': ['43021-01'], # REV - Storage Income
},
{
    'new_col_name': 'Revenues w/o VAT - Other Income',
    'codes': ['41310-10', # REV - Lease Cancelations 
              '42051-10', # REV - Tenant Work Order 
              '42480-10', # REV - Miscellaneous Income 
              '42510-10', # REV - Key Income
              '42515-10', # REV - Application Fee 
              '42560-10', # REV - Tenant Damage Income 
              '43013-20', # REV - Pet Rent 
              '43021-02'], # REV - Facility Use Fee
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
    'codes': ['41410-20', # REV - Cam Recovery-Estimate
              '41130-20'], # REV - Rental - Additional Services
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
    'new_col_name': 'OpEx - Payroll',
    'codes': ['51110-10', # Cleaning-Payroll
              '61110-10', # Cleaning-Payroll
              '51110-15', # Cleaning-Contract Service
              '61110-15', # Cleaning-Contract Service
              '62110-10', # R&M-Payroll-Salaries
              '62140-10', # R&M-Payroll-Outside Contract
              '65110-10', # Administrative-Payroll-Salaries
              '65120-10', # Administrative-Payroll-Reimbursed-Labor
              '65140-10' # Administrative-Payroll-Outside Contract
              '55330-10', # Other Professional Fees
              '65330-10'], # Other Professional Fees
    'factor': -1
},
{
    'new_col_name': 'OpEx - Marketing',
    'codes': ['68220-10', # Advertising & Promo
              '68330-10'], # Marketing
    'factor': -1
},
{
    'new_col_name': 'OpEx - Repairs & Maintenance',
    'codes': ['52210-20', # Elevator/Escalator-Service Contracts
              '62210-20', # Elev-Service Contract
              '52610-20' # Plumbing-Service Contract
              '62610-20' # Plumbing-Service Contract
              '52610-40' # Plumbing-Repairs & Maintenance
              '62610-40' # Plumbing-Repairs & Maintenance
              '52710-20', # Fire & Safety-R&M Contract
              '62710-20', # Fire & Safety-R&M Contract
              '62710-40', # Fire & Safety-Repairs & Maintenance
              '62710-50', # Fire & Safety-Supplies & Materials
              '63990-20', # Repairs And Maintenance
              '52810-20', # Pest Control-Contract
              '62810-20', # Pest Control-Contract
              '54210-20', # Landscaping-Gardening Contract
              '64210-20', # Landscaping-Gardening Contract
              '64245-10', # Turn-Over--Painting
              '64230-20'], # Pool-Service Contract
    'factor': -1
},
{
    'new_col_name': 'OpEx - Office Expenses',
    'codes': ['51110-40', # Cleaning-Repairs&Maintenance
              '61110-40', # Cleaning-Repairs&Maintenance
              '51110-50', # Cleaning-Supplies&Materials
              '61110-50', # Cleaning-Supplies&Materials
              '53120-10', # Bldg R&M (Interior)-Lock & Keys
              '63120-10', # Bldg R&M (Interior)-Lock & Keys
              '63160-10', # Bldg R&M (Interior)-Supplies & Materials
              '63165-10', # Bldg R&M (Interior)-Uniforms
              '53180-30', # Bldg R&M (Interior)-Generator
              '63180-30', # Bldg R&M (Interior)-Generator
              '54140-10', # Telephone
              '64140-10', # Telephone
              '54820-10', # Supplies & Materials
              '64820-10', # Supplies & Materials
              '65310-10', # Accounting/Tax
              '95200-15', # OI&E - Appraisal Fee (category 9)
              '65320-10', # Legal Fees
              '65330-10', # Other Professional Fees
              '65420-10', # Office Furniture/Equipment Rental
              '65405-10', # Meals & Entertainment
              '65410-20', # Office Employee Parking
              '65430-10', # Office Supplies
              '65440-10', # Office Expense
              '65440-95', # Telecom/Internet
              '65465-10', # Credit Card Fee
              '65470-10', # License, Permit, & Fees
              '65480-10', # Postage/Messengerial
              '65550-10'], # Training & Seminar
    'factor': -1
},
{
    'new_col_name': 'OpEx - Utilities',
    'codes': ['54110-10', # Electricity
              '64110-10', # Electricity
              '54120-10', # Gas
              '64120-10', # Gas
              '54130-10', # Water/Sewer
              '64130-10'], # Water/Sewer
    'factor': -1
},
{
    'new_col_name': 'OpEx - Others',
    'codes': ['61400-10', # Miscellaneous - Covid19
              '65050-30', # Non Creditable Vat
              '65060-10', # Late Fees
              '65610-10', # Travel - General (Employee Expenses)
              '65630-10', # Auto Expense, Parking & Mileage
              '65630-11', # Non-Deductible Reimbursements
              '68260-10', # Tenant Activity/Relations
              '68290-10', # Tenant Subsidy
              '68230-11', # Meals & Enternainment from General Leasing Expense
              '70110-10', # C&GE - Legal Services (category 7)
              '93110-10'], # OI&E - Bank Charges (category 9)
    'subtract_codes': ['91010-10', # OI&E - Interest Income-Investment (category 9) (negative in model)
                       '91050-10'], # OI&E - Interest Income-Others (category 9) (negative in model)
    'factor': -1
},
{
    'new_col_name': 'OpEx - Property Management Fee',
    'codes': ['65215-10'], # Property Mgmnt Fee-3Rd Party
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
    'codes': ['67110-10'], # Real Estate Taxes
    'factor': -1
},
{
    'new_col_name': 'SG&A - Insurance',
    'codes': ['67230-10'], # Property Insurance
    'factor': -1
},
{
    'new_col_name': 'SG&A - Leasing Comissions',
    'sum_columns': ['Revenues w/ VAT', 'Revenues w/o VAT'],
    'factor': -0.025
},
{
    'new_col_name': 'SG&A - Total',
    'sum_columns': ['SG&A - Real Estate Taxes', 'SG&A - Insurance', 'SG&A - Leasing Comissions']
},
{
    'new_col_name': 'Total Revenue',
    'sum_columns': ['Revenues w/ VAT', 'Revenues w/o VAT', 'Maintenance']
}
]