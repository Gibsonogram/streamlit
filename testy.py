import pandas as pd
from datetime import datetime
import numpy as np
import altair as alt
import altair_viewer




big_tuna = pd.read_csv("wsb_ticker_mentions.csv")

print(big_tuna)
# big_tuna['date_hour'] = bt_date
# big_tuna.to_csv("wsb_ticker_mentions.csv", index=False, na_rep=0)

