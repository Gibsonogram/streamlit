import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

"""
spy = pd.read_csv('historical_data/SPY.csv', usecols=[0,4])
spy = spy.tail(150)

fig, ax = plt.subplots()

ax.set_xlim((100, len(spy)+200))

xticks = [date for index, date in enumerate(spy['Date']) if index % 50 == 0]

ax.set_xticklabels(xticks)

sns.regplot(x = spy.index, y = 'Close', data = spy, ci=None, truncate=False)
plt.show() 
"""
