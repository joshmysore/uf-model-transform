def sorting_key(column_name):
    # Ignore column names that don't follow the correct format
    if not re.match(r'^[56]\d{4}-\d{2}: ', column_name):
        return float('inf'), float('inf')
    # Extract code and subcode from column name
    code, subcode = map(int, column_name.split(': ')[0][1:].split('-'))
    return code, subcode

# Iterate over the sorted_columns
original_columns = sorted_columns.copy()

for i in range(len(sorted_columns) - 1):
    # Check if there is a pair of '5' and '6' codes
    code_i = sorted_columns[i].split(':')[0]
    code_i_plus = sorted_columns[i + 1].split(':')[0]
    
    if code_i.startswith('5') and code_i_plus.startswith('6') and code_i[1:] == code_i_plus[1:]:
        # Create the new column name
        new_col = 'SUM: ' + sorted_columns[i] + ' & ' + sorted_columns[i+1]

        # Add the new column to the DataFrame
        output_df[new_col] = output_df[sorted_columns[i]] + output_df[sorted_columns[i+1]]
        
        # Append the new column to the sorted_columns list
        sorted_columns.insert(i+2, new_col)

# Remove columns that were used in the summations
columns_to_remove = [col for col in original_columns if any(col in sum_col for sum_col in sorted_columns if sum_col.startswith('SUM'))]
output_df.drop(columns_to_remove, axis=1, inplace=True)

# Get all columns that need to be sorted
sorted_columns = [column for column in output_df.columns if column.startswith('5') or column.startswith('6')]

# Sort the columns
sorted_columns.sort(key=sorting_key)

# Add the 'SUM' columns to the end of the list
sorted_columns += [column for column in output_df.columns if column.startswith('SUM')]

# Reorder the DataFrame
output_df = output_df[sorted_columns]