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
    for submi in reddit.subreddit(sub).new(limit=post_lim):
        search_res = ticker_search(sub, 1)
        if search_res:
            print(search_res)
        else:
            print('no stocks mentioned in that post')

sentiment_score(wsb, 5)




        