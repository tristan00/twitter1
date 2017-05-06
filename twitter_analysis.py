import requests
import time
import json
import random
from bs4 import BeautifulSoup
import datetime
from json import loads
import traceback
import requests
import random
import sys
from urllib.error import URLError
from TwitterSearch import *
import pytz
import sqlite3
import twitter
import birdy
#from birdy.twitter import UserClient
from queue import Queue
from threading import Thread

access_token = None
access_token_secret = None
consumer_key = None
consumer_secret = None
#twitter_base_url = 'https://twitter.com/{0}'

def get_auth():
    global access_token
    global access_token_secret
    global consumer_key
    global consumer_secret

    conn = sqlite3.connect('auth.db')
    cursor = conn.cursor()
    fields = cursor.execute('select * from authentication')

    for i in fields:
        #fields_dict[i[0]] = i[1]
        if i[0] == 'API Key':
            consumer_key = i[1]
        if i[0] == 'API Secret':
            consumer_secret = i[1]
        if i[0] == 'Access Token':
            access_token = i[1]
        if i[0] == 'Access Token Secret':
            access_token_secret = i[1]

def main():
    get_auth()
    #print(consumer_key, consumer_secret, access_token, access_token_secret)
    tuo = TwitterUserOrder('BarackObama')

    ts = TwitterSearch(consumer_key,
                    consumer_secret,
                    access_token,
                    access_token_secret)

    for tweet in ts.search_tweets_iterable(tuo):
        print(tweet)
        return



main()