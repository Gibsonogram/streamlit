import praw as pr
import pandas as pd
from datetime import datetime
import time

reddit = pr.Reddit(client_id = '5lMt_1-JSba0hw',
                   client_secret = 'tkWQfmM_67BLdoxrOpAVQb7V13GsLQ',
                   username = 'Iwillnotbeaplankton',
                   password = 'Snowdrop1',
                   user_agent = 'first_app')

wsb = reddit.subreddit('wallstreetbets')
date_w_hour = datetime.now().strftime('%m/%d %H:00')

richard = pd.read_csv("ticker_list.csv")
richard.columns = ['tickers']
tickers_final = richard['tickers'].tolist()

start = time.perf_counter()

def ticker_searcher(post_lim=50):
    mentions = []
    tickoo = tickers_final[:4221]
    tickoo2 = []
    for ticker in tickoo:
        ticker = ticker[1:]
        tickoo2.append(ticker)
    tickoo = tickoo2
    mentions_wo_space = []

    for submi in wsb.new(limit=post_lim):
        #this litle ditty adds any post beginning with a ticker to mentions_wo_space
        for ticker in tickoo:
            if ticker in submi.title[:6] \
            and ticker[0] == submi.title[0]:
                mentions_wo_space.append(ticker)
                break
        #this big boy does the main search
        mention_in_submission = "just initializing"
        for ticker in tickers_final:
            if ticker in submi.title:
                #following if block is needed because both 'stock' and '$stock' are in tickers_final
                if ticker == "$" + mention_in_submission:
                    continue
                mention_in_submission = ticker
                mentions.append(ticker)
                # print(ticker + "https://www.reddit.com" + submi.permalink)

    # updating 'mentions' so that it sees '$stock' and ' stock' as identical
    # also mentions_wo_space may already have some tickers in it.
    for ticker in mentions:
        ticker = ticker[1:]
        mentions_wo_space.append(ticker)
    mentions = mentions_wo_space

    # counting repeats from mentions
    repeats = []
    for ticker in mentions:
        if mentions.count(ticker) > 1 \
        and ticker not in repeats:
            repeats.append(ticker)
            # print(ticker, mentions.count(ticker))

    big_tuna = pd.read_csv("wsb_ticker_mentions.csv")
    #popping this date column so it doesn't fuck my calculations.
    bt_date = big_tuna.pop('date_hour')

    #this updates the dataframe and writes the new version to the csv
    new_row = len(big_tuna)
    for ticker in mentions:
        if ticker in mentions:
            big_tuna.at[new_row, ticker] = mentions.count(ticker)
            if ticker not in big_tuna.columns.tolist():
                big_tuna[ticker] = 0

    #organize big_tuna by whatever was mentioned most in latest row
    big_tuna = big_tuna.sort_values(by = new_row, axis=1, ascending=False)

    #add the date col back in and other tidying.
    big_tuna = big_tuna.fillna(0)
    big_tuna = big_tuna[:].astype(int)
    big_tuna['date_hour'] = bt_date
    big_tuna.at[new_row, 'date_hour'] = date_w_hour
    # print(big_tuna)

    big_tuna.to_csv("wsb_ticker_mentions.csv", index=False, na_rep=0)



ticker_searcher(500)
finish = time.perf_counter()

print(f'function took {round(finish - start, 2)} seconds')