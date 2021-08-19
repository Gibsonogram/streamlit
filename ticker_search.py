import praw as pr
import pandas as pd
from config import *
import time

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
ticker_list = pd.read_csv("ticker_list.csv", names=['tickers']) # get this from an api that is updated
tickers = ticker_list['tickers']

start = time.perf_counter()

def ticker_search(sub, post_lim=50):
    """Searches through a given subreddits n newest post titles for stock tickers.
    
    Params
    -----------
    Subreddit (required): which subreddit to search through. 
    Searches 'new' posts.
    post lim (optional): Defaults to 50. How many posts to search through. Linear time.
    Could be optimized.

    Returns
    --------
    Array of (ticker, count) tuples."""

    mentions = []
    for submi in reddit.subreddit(sub).new(limit=post_lim):
        # this big boy does the main search
        # submi.title is a str
        title = submi.title
        
        for ticker in tickers:
            if ticker in title:
                ticker_b = title.index(ticker[0])
                ticker_e = title.index(ticker[-1])
                
                # handles the edge cases of ticker at the end of post tile.
                if title[ticker_e] == title[-1]:
                    if title[ticker_b] == 0:
                        #this would be the ridiculous case of the post title simply being a stock title. That's dumb and I don't want it in my data.
                        continue
                    elif title[ticker_b - 1].isspace() or title[ticker_b - 1] == '$':
                        mentions.append(ticker)
                
                # every other case
                elif title[ticker_e + 1].isspace():
                    if ticker_b == 0:
                        mentions.append(ticker)
                    elif title[ticker_b - 1].isspace() or title[ticker_b - 1] == '$':
                        mentions.append(ticker)
    
    for ticker in mentions:
        counts = [mentions.count(i) for i in set(mentions)]
        ticker_counts = list(zip(set(mentions), counts))
    
    return ticker_counts



ticker_search(wsb, 100)
finish = time.perf_counter()
print(finish)
