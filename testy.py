import pandas as pd
from datetime import datetime
import numpy as np
import altair as alt
import altair_viewer
import time

goop = [[1,2,3],
        [4,5,6]]

def goop_appender(ls):
    goop.append(ls)



big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
print(big_tuna)
# big_tuna = big_tuna.drop(big_tuna.index[50:])
print(big_tuna)

# big_tuna.to_csv("wsb_ticker_mentions.csv", index=False, na_rep=0)

