from collections import UserDict
from numpy.core.numeric import full
import praw as pr
import pandas as pd
from config import *
import time
import re

# reddit api
reddit = pr.Reddit(client_id = CLIENT_ID,
                   client_secret = CLIENT_SECRET,
                   username = USERNAME,
                   password = PASSWORD,
                   user_agent = USER_AGENT)

# some subreddits
wsb = 'wallstreetbets'
stocks = 'stocks'
ssb = 'smallstreetbets'

# params
ticker_list = pd.read_csv("ticker_list.csv", usecols=['ticker', 'name'])
ticker_list = ticker_list[ticker_list['ticker'].str.len() > 1]
tickers = ticker_list['ticker']
stock_names = ticker_list['name'].str.lower()

# start = time.perf_counter()


def ticker_search(post_title: str):
    """
    Searches through given string for stock names/ticker mentions
    
    Returns: array of [ticker, name] elements for each ticker or name it finds.
    """
    mentions = []
    for ticker, stock_name in list(zip(tickers, stock_names)):
        lowered = post_title.lower()

        # Checks if the ticker is in the post_title
        if ticker in post_title:
            ticker_b = post_title.index(ticker[0])
            ticker_e = post_title.index(ticker[-1])
            
            # handles the edge cases of ticker/name at the end of post tile.
            if post_title[ticker_e] == post_title[-1]:
                if post_title[ticker_b] == 0:
                    #this would be the ridiculous case of the post post_title simply being a stock post_title. That's dumb and I don't want it in my data.
                    break
                elif post_title[ticker_b - 1].isspace() or post_title[ticker_b - 1] == '$':
                    mentions.append([ticker, stock_name])
            
            # every other case where ticker or stock name can appear.
            elif post_title[ticker_e + 1].isspace():
                if ticker_b == 0:
                    mentions.append([ticker, stock_name])
                elif post_title[ticker_b - 1].isspace() or post_title[ticker_b - 1] == '$':
                    mentions.append([ticker, stock_name])
        
        # else if the stock name is in the post_title. It only needs to see one or the the other.
        elif stock_name in lowered and stock_name != 'the':
            name_b = lowered.index(stock_name[0])
            name_e = lowered.index(stock_name[-1])

            if lowered[name_e] == post_title[-1]:
                #Again, this would be the useless case of the post_title being the stock name.
                if lowered[name_b] == 0:
                    break
                elif lowered[name_b - 1].isspace():
                    mentions.append([ticker, stock_name])
            
            elif lowered[name_e].isspace():
                if name_b == 0 or lowered[name_b - 1].isspace():
                    mentions.append([ticker, stock_name])

    return mentions


# x = ticker_search('the favorite GME')
# print(x)