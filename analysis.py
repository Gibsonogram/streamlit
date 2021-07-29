from matplotlib import rcParams
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# params
ticker = 'GME'
# plt.figure(figsize=(11,5))
shift_num = 17



# data is D OHLC
big_tuna = pd.read_csv('wsb_ticker_mentions.csv')
bt_cols = big_tuna.columns

csv_data = pd.read_csv(f'historical_data/{ticker}.csv')
closes = []
for i in csv_data['Close']:
    closes.append(round(float(i), 2))
tick_num = 15
ticks = [tick[-5:] for index, tick in enumerate(csv_data['Date']) if index % tick_num == 0]

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


to_file = pd.DataFrame()
to_file['close'] = csv_data.values
to_file[f'{shift_num} day shifted mentions'] = mention_series.values
to_file['dates'] = csv_data.index

# getting variants
if ticker == 'NVDA':
    l_ticker = str(ticker).lower()
    to_file.to_csv(f"correlation_dataframes/{l_ticker}_data.csv", index=False, na_rep=0)






csv_diff = csv_data.diff()




shifted_back = mention_series.shift(-shift_num)
# print(mention_series, shifted_back)
# that was a shit show...
x = round(pd.Series.corr(shifted_back, csv_data), 2)

doop = len(shifted_back) - len(shifted_back.dropna())
dom = np.array(shifted_back.dropna().values)
ran = np.array(csv_data.tail(len(csv_data)-doop).values)
print(dom, ran)
m, b = np.polyfit(dom, ran, 1)

print(shift_num, x, len(shifted_back.dropna()))

ax, fig = plt.subplots()

my_dict = {'a' : 1, 'b' : 2}

plt.scatter(dom, ran)
plt.plot(dom, dom*m + b)
plt.show()



"""

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time')
ax1.set_ylabel(f'{ticker} mentions on wsb', color=color)
ax1.plot(mention_series.index, mention_series.values, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel(f'{ticker} price', color=color)  # we already handled the x-label with ax1
ax2.plot(mention_series.index, csv_data.values, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.xticks(ticks=ticks)
plt.title(f'{ticker}')
plt.show()
"""