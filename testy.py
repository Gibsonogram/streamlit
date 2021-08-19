import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import praw
from ticker_search import ticker_search
import fuzzywuzzy

def sentiment_score(subreddit):
    
    ticker_search(subreddit, 1)