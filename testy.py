import pandas as pd
from datetime import datetime
import numpy as np

big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
big_tuna = big_tuna.drop('date_hour', axis=1)



big_ticket = []


#print(big_tuna.iat[-17,3])

ls = [1,2,3,4,5]
print(ls[1:])

def func():
    """fgssf"""
    return
print(func.__doc__)