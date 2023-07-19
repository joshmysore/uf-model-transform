import pandas as pd
from model import get_file_path, load_dataframe, find_code_column, group_data_by_code, fetch_exchange_rate, populate_data_dict, create_output_dataframe, create_custom_columns, export_to_excel
from columns_defs import column_definitions

def main():
    # read dataframe from fucntions defined
    file_path = get_file_path()

    # load dataframe
    df = load_dataframe(file_path)

    # find code column
    code_column, code_prefixes, groups = find_code_column(df)

    # group data by code
    groups = group_data_by_code(df, code_column, code_prefixes, groups)

    # fetch dates from populate_data_dict
    dates = []
    divisors = fetch_exchange_rate(dates)

    # Initialize an empty DataFrame
    output_df = pd.DataFrame()

    # reverse the order of the groups to print in correct order on the spreadsheet
    group_keys = sorted(groups.keys(), reverse=True)

    for group_key in group_keys:
        data_dict, dates = populate_data_dict(df, code_column, groups[group_key]["codes"], dates)
        temp_df = create_output_dataframe(data_dict, groups[group_key]["final"])
        # Merge temp_df with output_df here
        output_df = pd.concat([temp_df, output_df], axis=1)

    new_position = 0  # specify new_position

    # create custom columns
    output_df = create_custom_columns(output_df, divisors, new_position, column_definitions)

    desired_column_order = [col_def['new_col_name'] for col_def in column_definitions]
    # This will create a list of column names in the order they appear in column_definitions.

    # Add any other columns from your DataFrame that aren't included in column_definitions.
    for column in output_df.columns:
        if column not in desired_column_order:
            desired_column_order.append(column)

    # Reorder the columns in your DataFrame.
    output_df = output_df[desired_column_order]

    # Export to excel
    export_to_excel(output_df, file_path)

if __name__ == "__main__":
    main()