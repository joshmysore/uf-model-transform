from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd

api_key = '5TLIDN7TN6IQZJUE'

fx = ForeignExchange(key=api_key, output_format='pandas')

data = fx.get_currency_exchange_daily('CLF', 'CLP', outputsize='full')

print(data)

