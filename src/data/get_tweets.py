# -*- coding: utf-8 -*-
"""
Created on Mon May 31 15:08:38 2021

@author: Mayuresh
"""

import numpy as np
import pandas as pd
import requests
import json
import tweepy as tw
from datetime import date, datetime, timedelta
import time
from tqdm import tqdm


consumer_key = 'x0peUiFDesINygzpbApJbKnQl'
consumer_secret = 'AAR3yI6va9X9b0l04x3NC5ygsaSTHUm6J5nEZExHXcnzvGDCnG'
access_token = '162618833-15zdk4re05fq6demG9ItbjFVtRhaoNaDZy78At3w'
access_token_secret = 'BPfsLYUAup4SQx9urpno0nAXL9yc1j3GssDfSohz9aJyc'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)

df_tweets = pd.DataFrame(
    columns={'tweet_text', 'created_at', 'favorite_count'})


search_words = "doge OR dogecoin -filter:retweets -RT -retweet -retweets"

for N_DAYS_AGO in tqdm(range(0, 8)):
    today = date.today()
    date_until = today - timedelta(days=N_DAYS_AGO)
    date_since = date_until - timedelta(1)
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       since=date_since,
                       until=date_until,
                       tweet_mode="extended").items(890)
    for tweet in tweets:
        df_tweets = df_tweets.append({'created_at': tweet.created_at,
                                      'tweet_text': tweet.full_text,
                                      'favorite_count': tweet.favorite_count},
                                     ignore_index=True)
    df_tweets.to_csv('df_tweets_{}.csv'.format(N_DAYS_AGO), index=False)
    time.sleep(15*60)

df_tweets.to_csv('df_tweets.csv', index=False)
