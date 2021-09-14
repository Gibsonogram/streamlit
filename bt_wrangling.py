import distutils
from os import close
from PIL.Image import new
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

stock = 'NVDA '

bt_data = pd.read_csv('wsb_ticker_mentions.csv', usecols=[stock, 'date_hour'])
actual = pd.read_csv('historical_data/nvda.csv', usecols=['Close', 'Date'])

# reindex Date in the same format as the bt_dates
new_dtf = [i.split('-', 1) for i in actual['Date']]
actual['Date'] = [j for [i, j] in new_dtf]
bt_data['Date'] = bt_data['date_hour'].str.split(' ').str[0]
bt_data['Date'] = bt_data['Date'].str.replace('/','-')
bt_data = bt_data.drop('date_hour', axis=1)

bt_data = bt_data.drop_duplicates(subset='Date', keep='last')

# making a df of usable dates - closes - mentions
def intersection(ls1, ls2):
    ls3 = [i for i in ls1 if i in ls2]
    return ls3

mentions=[]
shared_dates = intersection(bt_data['Date'].values, actual['Date'].values)
for ind, date in enumerate(bt_data['Date'].values):
    if date in shared_dates:
        mentions.append(bt_data.iloc[ind, 0])
closes = []
for ind, date in enumerate(actual['Date'].values):
    if date in shared_dates:
        closes.append(actual.iloc[ind, 1])

# usable combined df
combined = pd.DataFrame()
combined['Date'] = shared_dates
combined['Close'] = closes
combined['Mentions'] = mentions


# combined.to_csv(f'correlation_dataframes/{stock.lower()}_data.csv', index=False)






