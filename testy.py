import pandas as pd
from datetime import datetime
import numpy as np



big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
bt_date = big_tuna.pop('date_hour')



big_tuna = big_tuna.drop(big_tuna.tail(1).index, axis=0)




big_tuna['date_hour'] = bt_date

print(big_tuna)

big_tuna.to_csv("wsb_ticker_mentions.csv", index=False, na_rep=0)