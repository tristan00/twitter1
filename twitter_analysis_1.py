import nltk
import sqlite3
import collections
import operator
import traceback



def RE(text):
    #Flesch Reading Ease Readability Formula
    #RE = 206.835 – (1.015 x ASL) – (84.6 x ASW)
    ASL = 0
    ASW = 0

    ASL = sum(len(sent) for sent in nltk.corpus.inaugural.sents(text)) / len(nltk.corpus.inaugural.sents(text))

    RE = 206.835 - (1.015*ASL) - (84.6*ASW)


def lexical_diversity(text):
    return len(set(text)) / len(text)

def get_tweets():
    conn = sqlite3.connect('twitter.db')
    cursor = conn.cursor()
    users = cursor.execute('select DISTINCT user from twitter_data').fetchall()
    users_dict= {}

    for u in users:
        fields = cursor.execute('select * from twitter_data where user = ?', u).fetchall()
        users_dict[u[0]] = []
        for i in fields:
            users_dict[u[0]].append((i[1], i[2]))
    conn.close()
    return users_dict

def print_tweets():
    conn = sqlite3.connect('twitter.db')
    cursor = conn.cursor()
    users = cursor.execute('select DISTINCT user from twitter_data').fetchall()
    for u in users:
        fields = cursor.execute('select * from twitter_data where user = ?', u).fetchall()
        print(u[0], len(fields))
        for i in fields:
            print(u[0], i[1])

def analyze_profile(user, user_data):
    #get most responded to/retweeted accounts
    most_retweeted = {}
    most_retweeted_list = []
    for i in user_data:
        if i[1] == None:
            continue
        try:
            most_retweeted[i[1]] += 1
        except:
            most_retweeted[i[1]] = 1
    #make top 10 connections
    for key in most_retweeted.keys():
        temp = (key, most_retweeted[key])
        most_retweeted_list.append(temp)
    most_retweeted_list = sorted(most_retweeted_list, key=lambda tweeted: tweeted[1], reverse=True)

    #text analysis
    cleaned_text = '' # remove links, twitter handles, add punctuation in between tweets

    for i in user_data:
        try:
            temp_text_list = i[0].replace('"','').replace("'",'').replace("(",'').replace(")",'').replace("-",'').replace("_",'').split(' ')
            result =  filter(lambda x:('#' not in x and '@' not in x and 'http' not in x), temp_text_list)
            result_str = ' '.join(list(result))
            if '.' not in result_str[-2:]:
                result_str = result_str + '. '
        except:
            traceback.print_exc()
        cleaned_text += result_str

    lexical_diversity_value = lexical_diversity(cleaned_text)
    print(user, lexical_diversity_value)
    print('most interacted with: ')
    for i in most_retweeted_list[:3]:
        print(i[0], i[1])

    print()
    print()
    print()



def main():
    users_dict = get_tweets()

    for u in users_dict.keys():
        analyze_profile(u, users_dict[u])

main()

#a = "Hello all please help #me ".split(' ')
#b = filter(lambda x:x[0]!='#', a.split())
#print([item for item in a if item[0]!='#'])
