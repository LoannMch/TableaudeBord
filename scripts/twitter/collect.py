# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import tweepy
import pandas as pd
import api_key

Consumer_key = api_key.Consumer_key
Consumer_secret = api_key.Consumer_secret

# externaliser les consumer key


def collect_tweets(requete, nb_tweets, Consumer_key, Consumer_secret):
    authentication = tweepy.OAuthHandler(consumer_key = Consumer_key, 
                                         consumer_secret = Consumer_secret)
    api = tweepy.API(authentication)
    lst_tweets = []
    for tweet in tweepy.Cursor(api.search, q = requete).items(nb_tweets):
        lst_tweets.append(tweet)
    return lst_tweets

def choose_langage(data_set, langage):
    return data_set[data_set.langage == langage]
    
    
def process_tweets(lst_tweets):
    id_list = [tweet.id for tweet in lst_tweets]
    data_set = pd.DataFrame(id_list, columns=["id"])   
    data_set["text"] = [tweet.text for tweet in lst_tweets]
    data_set["date"] = [tweet.created_at for tweet in lst_tweets]
    data_set["langage"] = [tweet.lang for tweet in lst_tweets]
    data_set["retweet_count"] = [tweet.retweet_count for tweet in lst_tweets]
    choose_langage(data_set, 'en')
    return(data_set)

tweets = collect_tweets('WannaCry', 10,  Consumer_key ,Consumer_secret)
data =  process_tweets(tweets)

print(data)
data.to_json(path_or_buf = "tweets.json")

