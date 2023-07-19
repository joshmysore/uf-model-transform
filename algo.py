import pandas as pd
from model import *
from columns_defs import *

def main():
    # leer dataframe desde las funciones definidas
    file_path = get_file_path()

    # cargar dataframe
    df = load_dataframe(file_path)

    # encontrar la columna de código
    code_column, code_prefixes, groups = find_code_column(df)

    # agrupar datos por código
    groups = group_data_by_code(df, code_column, code_prefixes, groups)

    # obtener fechas desde populate_data_dict
    dates = []
    divisors = fetch_exchange_rate(dates)

    # Inicializar un DataFrame vacío
    output_df = pd.DataFrame()

    # invertir el orden de los grupos para imprimir en el orden correcto en la hoja de cálculo
    group_keys = sorted(groups.keys(), reverse=True)

    for group_key in group_keys:
        data_dict, dates = populate_data_dict(df, code_column, groups[group_key]["codes"], dates)
        temp_df = create_output_dataframe(data_dict, groups[group_key]["final"])
        # Fusionar temp_df con output_df aquí
        output_df = pd.concat([temp_df, output_df], axis=1)

    new_position = 0  # especificar new_position

    # crear columnas personalizadas
    output_df = create_custom_columns(output_df, divisors, new_position, column_definitions)

    desired_column_order = [col_def['new_col_name'] for col_def in column_definitions]
    # Esto creará una lista de nombres de columnas en el orden en que aparecen en column_definitions.

    # Añadir cualquier otra columna de su DataFrame que no esté incluida en column_definitions.
    for column in output_df.columns:
        if column not in desired_column_order:
            desired_column_order.append(column)

    # Reordenar las columnas en su DataFrame.
    output_df = output_df[desired_column_order]

    # Exportar a Excel
    export_to_excel(output_df, file_path)

if __name__ == "__main__":
    main()