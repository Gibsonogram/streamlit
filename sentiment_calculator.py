from numpy.core.defchararray import lower
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import praw as pr
from ticker_search import ticker_search
import fuzzywuzzy
from config import *

reddit = pr.Reddit(client_id = CLIENT_ID,
                   client_secret = CLIENT_SECRET,
                   username = USERNAME,
                   password = PASSWORD,
                   user_agent = USER_AGENT)

wsb = 'wallstreetbets'


def sentiment_score(sub, post_lim):
    titles = [i.title for i in reddit.subreddit(sub).new(limit=post_lim)]
    # the following dict is based on the most common words in 500 wsb posts.
    sentiment_dict = {
        'positive' : ['bought', 'undervalued', 'breakout', 'long term', 'easy', 'free', 'sail', 'good', 'yolo', 'liftoff', 'green', 'moon', 'calls', 'all in', 'value', 'best', 'great', 'rocket'],
        'negative' : ['sold', 'overvalued', 'bad', 'puts', 'worst', 'bagholder', 'red', 'fail'],
        'ambiguous': ['meme', 'hold', 'joke']}

    stocks = []
    stock_names = []
    sentiments = []
    for title in titles:
        lowered = str(title).lower()
        search_res = ticker_search(title)
        # only search through title if the returned mentions is one stock.
        if len(search_res) == 1:
            # sentiment for any given post is given default value of 0.
            sentiment = 0
            ticker = search_res[0][0]
            stock_name = search_res[0][1]
            for pos in sentiment_dict.get('positive'):
                if pos in lowered:
                    sentiment += 1
            for neg in sentiment_dict.get('negative'):
                if neg in lowered:
                    sentiment -= 1
            if sentiment != 0:
                if ticker not in stocks:
                    stocks.append(ticker)
                    sentiments.append(sentiment)
                    stock_names.append(stock_name)
                else:
                    sent_index = stocks.index(ticker)
                    sentiments[sent_index] += sentiment
        else:
            continue
    
    df = pd.DataFrame()
    df['Stock'] = stock_names
    df['Ticker'] = stocks
    df['Sentiment'] = sentiments
    df = df.sort_values(by='Sentiment', ascending=False).set_index('Stock')
    
    return df


x = sentiment_score(wsb, 250)
print(x)



        