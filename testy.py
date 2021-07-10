import pandas as pd
from datetime import datetime
import numpy as np

big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
big_tuna = big_tuna.drop('date_hour', axis=1)



big_ticket = []

for col in big_tuna:
    for row in big_tuna[col]:
        if col not in big_ticket:
            if row > 22:
                big_ticket.append(col)

print(big_ticket)