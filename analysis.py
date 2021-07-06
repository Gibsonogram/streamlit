from matplotlib import rcParams
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.series import Series

# params
ticker = 'GME'
plt.figure(figsize=(11,5))
shift_num = 30



# get dat data
# data is D OHLC
big_tuna = pd.read_csv('wsb_ticker_mentions.csv')
bt_cols = big_tuna.columns
csv_data = pd.read_csv(f'historical_data/{ticker}.csv')
closes = []
for i in csv_data['Close']:
    closes.append(round(float(i), 2))
tick_num = 15
ticks = [tick for index, tick in enumerate(csv_data['Date']) if index % tick_num == 0]

csv_data = pd.Series(closes, index=csv_data['Date'])
for col in big_tuna.columns:
    if col == (ticker + ' '):
        mentions = big_tuna[col].values

# getting the same format for csv dates and bt dates
bt_dates = [entry[:2]+'-'+entry[3:5] for entry in big_tuna.iloc[:,-1]]
csv_dates = [entry[-5:] for entry in csv_data.index]
csv_data = pd.Series(closes, index=csv_dates)

mention_series = pd.Series(mentions, index=bt_dates)
d = []
v = []
for index, date in enumerate(mention_series.index):
    if date not in d:
        d.append(date)
        v.append(mention_series.values[index])
mention_series = pd.Series(v, index=d)

# now, same dates for csv file and mention_series
for i, j in list(zip(mention_series.index, csv_data.index)):
    if i not in csv_data.index:
        mention_series = mention_series.drop(i)
    if j not in mention_series.index:
        csv_data = csv_data.drop(j)

d = [date for date in mention_series.index]
v = []
for ind, val in zip(csv_data.index, csv_data.values):
    if ind in d:
        v.append(val)
csv_data = pd.Series(v, index=d)
# print(mention_series, csv_data)







shifted_back = mention_series.shift(-shift_num)
# print(mention_series, shifted_back)
# that was a shit show...
x = Series.corr(shifted_back, csv_data)
print(shift_num, x)

"""
plt.scatter(csv_data.values, shifted_back.values)
plt.xlabel('price')
plt.ylabel(f'mentions on wsb')
plt.title(f'{ticker}')
plt.show()
"""

"""
# this might come in handy... later
for row in range(0, len(big_tuna)):
    row_map = []
    for index, item in enumerate(big_tuna.iloc[row,:-1]):
        row_map.append([bt_cols[index], item])
    
    top_in_row = []
    for i, j in row_map:
        if j > 4:
            top_in_row.append([i,j])
    top_in_row.append(big_tuna.iat[row, -1])
    print(top_in_row)
"""
