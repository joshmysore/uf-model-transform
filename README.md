# README 

## Descripción general
Este proyecto consiste en tres archivos principales `functions.py`, `main.py`, y `new_columns.py` que son utilizados para la manipulación y el análisis de los datos contenidos en un DataFrame de pandas. El proceso de análisis incluye la carga de datos, el descubrimiento de columnas de códigos, la agrupación de datos por código, la creación de columnas personalizadas, la reordenación de columnas y la exportación de los resultados a un archivo de Excel.

## Descripción de los archivos

### functions.py
Este archivo contiene las funciones que se utilizan en el archivo `main.py` para la manipulación de datos.

Esta es una descripción detallada de cada función en los archivos proporcionados. Vamos a empezar con el archivo `functions.py`:

1. `get_file_path()`: Esta función abre una ventana de diálogo para seleccionar un archivo de Excel. Verifica que el archivo seleccionado sea un archivo de Excel y crea una nueva carpeta con el nombre "UF_modelo_{nombre de archivo original}_{fecha actual}". Cambia el directorio de trabajo a esta nueva carpeta y luego registra un archivo de registro con el nombre "log_{nombre del archivo}_{fecha y hora actual}". Al final, muestra un mensaje de confirmación de que el archivo se ha seleccionado y se ha leído en un dataframe.

2. `load_dataframe(file_path)`: Esta función carga el archivo de Excel seleccionado en un DataFrame de pandas.

3. `find_code_column(df)`: Esta función busca en el DataFrame la columna que contiene códigos basándose en el código de ingresos '40100-00'. Además, crea una lista de prefijos de códigos basados en el primer dígito del código y un diccionario de grupos basado en estos prefijos.

4. `group_data_by_code(df, code_column, code_prefixes, groups)`: Esta función agrupa los datos por código. Filtra las filas basándose en el código, crea un diccionario y llena las listas de los grupos correspondientes.

5. `populate_data_dict(df, code_column, codes, dates)`: Esta función llena un diccionario de datos con fechas como claves y diccionarios anidados como valores. Los diccionarios anidados contienen códigos como claves y valores correspondientes del DataFrame original como valores.

6. `fetch_exchange_rate(dates)`: Esta función obtiene las tasas de cambio mensuales desde un servidor externo y las devuelve como una lista de divisores. Si el servidor está caído, devuelve una lista de divisores por defecto.

7. `create_and_format_column(df, new_col_name, codes, divisors=None, rounding=0, position=None, factor=1., subtract_codes=None)`: Esta función crea y formatea una nueva columna en el DataFrame a partir de la suma de las columnas especificadas en 'codes', y resta las columnas especificadas en 'subtract_codes'. Además, aplica los divisores a los valores de la columna, multiplica los valores por un factor, redondea los valores y coloca la columna en una posición específica en el DataFrame.

8. `create_output_dataframe(data_dict, col_final)`: Esta función crea un DataFrame de salida con las fechas recogidas como filas y los códigos como columnas. Cambia el nombre de las columnas a los nombres finales, elimina todas las columnas que solo tienen un encabezado y no tienen datos, y elimina todas las columnas con la palabra "total" en el nombre.

9. `create_custom_columns(output_df, divisors, new_position, column_definitions)`: Esta función crea columnas personalizadas en el DataFrame de salida a partir de las definiciones de las columnas proporcionadas.

10. `style_and_save_excel(temp_filename, final_filename)`: Esta función aplica estilos a un archivo de Excel y lo guarda con un nuevo nombre.

11. `export_to_excel(output_df, filename)`: Esta función exporta el DataFrame de salida a un archivo de Excel y aplica estilos al archivo utilizando la función `style_and_save_excel`.

### main.py
Este archivo es el script principal que utiliza las funciones definidas en `functions.py` para realizar la manipulación y el análisis de los datos.

El script se inicia obteniendo la ruta del archivo a analizar con `get_file_path()`. Luego, carga el DataFrame con `load_dataframe(file_path)`. Encuentra la columna de código con `find_code_column(df)` y agrupa los datos por código con `group_data_by_code(df, code_column, code_prefixes, groups)`. Obtiene las fechas desde `populate_data_dict` y las tasas de cambio con `fetch_exchange_rate(dates)`. Después de inicializar un DataFrame vacío, invierte el orden de los grupos para imprimir en el orden correcto en la hoja de cálculo. Para cada grupo, crea un DataFrame temporal con `create_output_dataframe(data_dict, groups[group_key]["final"])` y lo fusiona con el DataFrame de salida. Crea columnas personalizadas con `create_custom_columns(output_df, divisors, new_position, column_definitions)` y reordena las columnas en el DataFrame de salida. Finalmente, exporta los datos a Excel con `export_to_excel(output_df, file_path)`.

### new_columns.py
Este archivo contiene una lista de diccionarios que definen nuevas columnas a ser creadas en el DataFrame. Cada diccionario especifica el nombre de la nueva columna, los códigos que deberían ser utilizados para calcular el valor de la columna, y cualquier factor que debería ser aplicado a los valores.

## Uso
Para usar este proyecto, simplemente ejecute el script `main.py`. Asegúrese de tener instaladas las bibliotecas de Python necesarias y tenga el archivo `new_columns.py` en el mismo directorio que `main.py` y `functions.py`.

## Dependencias de la biblioteca
Este proyecto depende de las siguientes bibliotecas de Python:
- pandas
- tkinter
- os
- requests
- datetime
- openpyxl
- tempfile
- logging

Instale las dependencias con pip usando el siguiente comando:
```
pip install pandas tkinter os requests datetime openpyxl tempfile logging
```

## Registro de eventos
Este proyecto utiliza la biblioteca `logging` de Python para registrar eventos. Los eventos se registran en el nivel INFO y se imprimen en la consola durante la ejecución del script.

## Transformación de datos
Los datos se transforman en varios pasos. Primero, los datos se cargan desde un archivo y se descubren las columnas de códigos. Los datos se agrupan por código y se crean nuevas columnas basadas en las definiciones en `new_columns.py`. Las columnas se reordenan según el orden especificado en `new_columns.py`, y los resultados se exportan a un archivo de Excel.

## Personalización
Puede personalizar este proyecto modificando `new_columns.py` para definir nuevas columnas. Asegúrese de especificar el nombre de la nueva columna, los códigos que deberían ser utilizados para calcular el valor de la columna, y cualquier factor que debería ser aplicado a los valores.

## Contribuciones futuras
Las contribuciones a este proyecto son bienvenidas. Si encuentra un error o tiene una sugerencia para una mejora, por favor abra un problema en el repositorio del proyecto.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia de CCLA.

## Contacto

Este programa fue creado por Josh Mysore, un estudiante de Havard, durante una pasantía con Compass en Julio 2023. Si tiene alguna pregunta o comentario sobre este proyecto, por favor póngase en contacto con el mantenedor actual del proyecto.