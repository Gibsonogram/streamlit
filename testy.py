import pandas as pd
from datetime import datetime
import numpy as np

big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
big_tuna = big_tuna.drop('date_hour', axis=1)



big_ticket = []

for col in big_tuna:
    for row in big_tuna[col]:
        if row > 10:
            if col in big_ticket:
                big_ticket.remove(col)
            break
        if 5 < row <= 10 and col not in big_ticket:
            big_ticket.append(col)


print(big_ticket)