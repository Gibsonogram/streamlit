import pandas as pd
from datetime import datetime
import numpy as np
import altair as alt
import altair_viewer




big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
bt_date = big_tuna.pop('date_hour')

tuna_chunk = big_tuna.iloc[:,:10].tail(10)

tuna_head = pd.DataFrame({"stock" : tuna_chunk.columns,
                              "mentions" : big_tuna.iloc[-1,:10]
                              })
print(big_tuna.iloc[:,:9])




#big_tuna = big_tuna.drop(big_tuna.tail(1).index, axis=0)
# big_tuna['date_hour'] = bt_date
# big_tuna.to_csv("wsb_ticker_mentions.csv", index=False, na_rep=0)