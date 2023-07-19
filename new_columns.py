column_definitions = [
{
    'new_col_name': 'UF',
    'divisor': True 
},
{
    'new_col_name': 'OpEx - Payroll',
    'codes': ['1110-10', # Cleaning-Payroll
              '1110-15', # Cleaning-Contract Service
              '1110-20', # Cleaning-Extra Service
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
    'codes': ['8220-10', # Advertising & Promo
              '8330-10'], # Marketing
    'factor': -1
},
{
    'new_col_name': 'OpEx - Repairs & Maintenance',
    'codes': ['2210-20', # Elevator/Escalator-Service Contracts
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
    'factor': -1
},
{
    'new_col_name': 'OpEx - Office Expenses',
    'codes': ['1110-40', # Cleaning-Repairs&Maintenance
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
    'factor': -1
},
{
    'new_col_name': 'OpEx - Utilities',
    'codes': ['4110-10', # Electricity
              '4120-10', # Gas
              '4130-10'], # Water/Sewer
    'factor': -1
},
{
    'new_col_name': 'OpEx - Others',
    'codes': ['1400-10', # Miscellaneous - Covid19
              '5050-30', # Non Creditable Vat
              '5060-10', # Late Fees
              '5610-10', # Travel - General (Employee Expenses)
              '5630-10', # Auto Expense, Parking & Mileage
              '5630-11', # Non-Deductible Reimbursements
              '8260-10', # Tenant Activity/Relations
              '8290-10', # Tenant Subsidy
              '8230-11', # Meals & Enternainment from General Leasing Expense
              '70110-10', # C&GE - Legal Services (category 7)
              '93110-10'], # OI&E - Bank Charges (category 9)
    'subtract_codes': ['91010-10', # OI&E - Interest Income-Investment (category 9) (negative in model)
                       '91050-10'], # OI&E - Interest Income-Others (category 9) (negative in model)
    'factor': -1
},
{
    'new_col_name': 'OpEx - Property Management Fee',
    'codes': ['5215-10'], # Property Mgmnt Fee-3Rd Party
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
    'codes': ['7110-10'], # Real Estate Taxes
    'factor': -1
},
{
    'new_col_name': 'SG&A - Insurance',
    'codes': ['7230-10'], # Property Insurance
    'factor': -1
},
{
    'new_col_name': 'SG&A - Leasing Comissions',
    'codes': [ # REVENUES W/O VAT
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
    'factor': -0.025
},
{
    'new_col_name': 'SG&A - Total',
    'sum_columns': ['SG&A - Real Estate Taxes', 'SG&A - Insurance', 'SG&A - Leasing Comissions']
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
    'codes': ['5050-10'], # Bad Debt Expense
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
    'new_col_name': 'Total Revenue',
    'sum_columns': ['Revenues w/ VAT', 'Revenues w/o VAT', 'Maintenance']
}
]