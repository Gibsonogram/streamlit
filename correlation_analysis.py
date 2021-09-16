from matplotlib import rcParams
from numpy.lib.function_base import corrcoef, diff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bt_wrangler import big_tuna_wrangler


# plt.figure(figsize=(11,5))

# maybe build a correlation finder...

def diff_n_shift(ticker, shift_num):
    """
    Differences and shifts series.
    Returns: DataFrame with all columns of interest
    
    Params
    -----------
    ticker: what ticker (from big tuna) to perform corr. analysis on.
    shift_num: how many days/sessions you want the data shifted back to. 

    shift_num: Amount of periods the series is shifted backward. 
    Ex: Entering 2 would give correlation between stock mentions and change in close-price as of two periods later. 
    Confused yet?
    """

    df = big_tuna_wrangler(ticker)
    closes = pd.Series(data=df['Close'].values, index=df['Date'])
    difference = closes.diff()
    df['Differenced'] = difference.values
    # We have the amount stock changed from previous period...
    # Now, we shift it forward designated amount and see if there is correlation
    shifted = difference.shift(shift_num)
    df['Shifted'] = shifted.values
    df[f'Shifted {shift_num}'] = df['Shifted']
    df = df.drop('Shifted', axis = 1)
    df = df.fillna(0)

    return df.iloc[shift_num+1:, :].reset_index(drop=True)


def corr_analysis(ticker):
    ticker = str(ticker).upper()
    correlations = []
    for x in range(1, 14):
        df = diff_n_shift(ticker, x)
        # col2 is mentions, col4 is shifted differenced closes.
        corr = np.corrcoef(df.iloc[:, 2], df.iloc[:, 4])
        correlations.append(round(corr[0][1], 4))
    
    delays = np.arange(1, 14)
    res = pd.DataFrame()
    res['Lag Period'] = delays
    res[f'{ticker} PCC'] = correlations
    return res


def corr_avg(ls_of_tickers):
    corr_values = pd.DataFrame(index=np.arange(1, 14))

    for ticker in ls_of_tickers:
        df = corr_analysis(ticker)
        corr_values[f'{ticker}'] = df[f'{ticker} PCC'].values

    corr_values['Mean'] = round(corr_values.mean(axis=1), 3)
    return corr_values




big_tuna = pd.read_csv('wsb_ticker_mentions.csv')
big_tuna = big_tuna.iloc[:, 5:15]
# print(big_tuna.columns)

high_mentions = ['SPCE', 'AMC', 'WISH', 'GME', 'NVDA']
mid_mentions = ['AAPL', 'CLF', 'BA', 'SHEN', 'TSLA', 'CLOV', 'CLNE', 'AMD', 'PUBM', 'NIO']
x = corr_avg(mid_mentions)
print(x)

# res.to_csv(f'correlation_dataframes/nvda_data.csv', index=False)

# plotting
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