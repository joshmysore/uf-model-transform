import pandas as pd

# Step 1: Read the spreadsheet into a DataFrame
df = pd.read_excel('input.xlsx')  # replace with the path to your Excel file

# Step 2: Convert the date column from strings to datetime objects
df['Date'] = pd.to_datetime(df['Date'], format='%b %Y')  # replace 'Date' with your date column name

# Step 3: Filter rows based on their "Recoverable Expenses" and "Nonrecoverable expenses" column values
recoverable_expenses = df[df['Category'] == 'Recoverable Expenses']  # replace 'Category' with your column name
nonrecoverable_expenses = df[df['Category'] == 'Nonrecoverable expenses']

# Step 4: Perform manipulations on the filtered data
# This is just an example, replace with your actual manipulations
recoverable_expenses['Total'] = recoverable_expenses.sum(axis=1)
nonrecoverable_expenses['Total'] = nonrecoverable_expenses.sum(axis=1)

# Step 5: Write the manipulated data to a new spreadsheet
recoverable_expenses.to_excel('recoverable_expenses.xlsx', index=False)
nonrecoverable_expenses.to_excel('nonrecoverable_expenses.xlsx', index=False)
