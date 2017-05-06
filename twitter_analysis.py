from TwitterSearch import *
import sqlite3
import traceback

access_token = None
access_token_secret = None
consumer_key = None
consumer_secret = None
ts = None # twitter connection object

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
    conn.close()

def read_users_tweets(user):
    tuo = TwitterUserOrder(user)

    #set up db connection
    conn = sqlite3.connect('twitter.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''CREATE TABLE twitter_data(user text, tweet text, reply_to text, PRIMARY KEY(user, tweet))''')
    except:
        #db already created
        pass


    for tweet in ts.search_tweets_iterable(tuo):
        user = tweet['user']['screen_name']
        tweet_text = tweet['text']
        try:
            reply_to = tweet['quoted_status']['user']['screen_name']
        except:
            reply_to = None

        try:
            cursor.execute('INSERT INTO twitter_data VALUES (?,?,?)', (user, tweet_text,reply_to))
            conn.commit()
        except:
            pass
            #traceback.print_exc()

    conn.close()


def get_tweet_count():
    conn = sqlite3.connect('twitter.db')
    cursor = conn.cursor()
    fields = cursor.execute('select * from twitter_data')
    print(len(fields.fetchall()))

def main():
    global ts

    get_auth()
    ts = TwitterSearch(consumer_key,consumer_secret,access_token,access_token_secret)

    users = ['BarackObama']
    for u in users:
        try:
            read_users_tweets(u)
        except:
            pass
    get_tweet_count()

main()

