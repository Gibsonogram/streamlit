import pandas as pd
from datetime import datetime
import numpy as np

big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
big_tuna = big_tuna.drop('date_hour', axis=1)
avg_arr = []

for col in big_tuna:
    col_sum = 0
    for item in big_tuna[col]:
        col_sum += item
    avg = round(col_sum / len(big_tuna),2)
    avg_arr.append([avg, col])

most_mentioned = [[i,j] for i,j in avg_arr if i > 3.5]
most_mentioned = pd.DataFrame(most_mentioned)


print(most_mentioned)