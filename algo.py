# create Payroll column
output_df['OpEx - Payroll'] = (
    output_df['51110-10: RE - Cleaning-Payroll'] +
    output_df['61110-10: NRE - Cleaning-Payroll'] +
    output_df['51110-15: RE - Cleaning-Contract Service'] +
    output_df['61110-15: NRE - Cleaning-Contract Service'] +
    output_df['62110-10: NRE - R&M-Payroll-Salaries'] +
    output_df['62140-10: NRE - R&M-Payroll-Outside Contract'] +
    output_df['65110-10: NRE - Administrative-Payroll-Salaries'] +
    output_df['65140-10: NRE - Administrative-Payroll-Outside Contract'] +
    output_df['55330-10: RE - Other Professional Fees'] +
    output_df['65330-10: NRE - Other Professional Fees']
)
output_df['OpEx - Payroll'] = output_df['OpEx - Payroll'] / 35510 
output_df['OpEx - Payroll'] = output_df['OpEx - Payroll'].round(0)

# place the column OpEx - Maintenance in the first column position
cols = output_df.columns.tolist()
cols.insert(0, cols.pop(cols.index('OpEx - Payroll')))
output_df = output_df.reindex(columns=cols)

# create Marketing column
output_df['OpEx - Marketing'] = (
    output_df['68220-10: NRE - Advertising & Promo'] + 
    output_df['68330-10: NRE - Marketing']
)
output_df['OpEx - Marketing'] = output_df['OpEx - Marketing'] / 35510
output_df['OpEx - Marketing'] = output_df['OpEx - Marketing'].round(0)

# place the column OpEx - Marketing in the second column position
cols = output_df.columns.tolist()
cols.insert(1, cols.pop(cols.index('OpEx - Marketing')))
output_df = output_df.reindex(columns=cols)

# create Repairs & Maintenance column
output_df['OpEx - Repairs & Maintenance'] = (
'2210-20',
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
'4245-10'
)