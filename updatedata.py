import tweepy as tw
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import csv
import pandas as pd
import json
from collections import OrderedDict
import datetime as DT
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

consumer_key = os.environ.get('API_KEY_TWITTER')
consumer_secret = os.environ.get('API_KEY_SECRET_TWITTER')
access_token = os.environ.get('ACCESS_TOKEN_TWITTER')
access_token_secret = os.environ.get('ACCESS_TOKEN_TWITTER_SECRET')

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_term = "$oxen -filter:retweets"
filepath = "/root/oxen-knights-website/"
raw_data = tw.Cursor(api.search,
                   q=search_term,
                   since=str(DT.date.today()- DT.timedelta(days=7))).items(5000)
print(raw_data)
TWEET_POINTS = 10
LIKE_POINTS = 1
RETWEET_POINTS = 5
MAX_POINTS = 150

def top_tweet(raw_data):
    top_points = 0

    print(len(raw_data[0]))
    for i in range(0,len(raw_data[0])):
        points = min(MAX_POINTS,(TWEET_POINTS + raw_data[3][i] * LIKE_POINTS + raw_data[4][i] * RETWEET_POINTS))
        if points > top_points and 'Defi_Eagle' != raw_data[2][i]:
            top_points = points
            top_tweet = {'points':points,'tweet_id':raw_data[0][i],'username':raw_data[2][i],'tweet':raw_data[1][i],'favorites':raw_data[3][i],'retweets':raw_data[4][i]}

    with open(filepath + 'toptweet.json', 'w') as F:
        F.write(json.dumps(top_tweet))
#'points':min(MAX_POINTS,(TWEET_POINTS + favorites[i] * LIKE_POINTS + retweets[i] * RETWEET_POINTS))}

## Take in new scraped data and add it to json file
def update_dataset(data):
    json_file =[[],[],[],[],[]]
    try:
        with open(filepath + 'data.json', 'r') as F:
            json_file = json.loads(F.read())
    except:
        print('no json file')
    for i in range(0,len(data[0])):
        if data[0][i] not in json_file[0]:
            json_file[0].append(data[0][i])
            json_file[1].append(data[1][i])
            json_file[2].append(data[2][i])
            json_file[3].append(data[3][i])
            json_file[4].append(data[4][i])
        else:
            json_file[1][json_file[0].index(data[0][i])] = data[1][i]
            json_file[2][json_file[0].index(data[0][i])] = data[2][i]
            json_file[3][json_file[0].index(data[0][i])] = data[3][i]
            json_file[4][json_file[0].index(data[0][i])] = data[4][i]


    with open(filepath +'data.json', 'w') as F:
        F.write(json.dumps(json_file))
    return json_file

def main():
    ids = []
    tweets=[]
    usernames = []
    favorites = []
    retweets = []
    for tweet in raw_data:
        if tweet.user.screen_name != 'Oxen_io':

            ids.append(tweet.id)
            tweets.append(tweet.text)
            favorites.append(tweet.favorite_count)
            retweets.append(tweet.retweet_count)
            usernames.append(tweet.user.screen_name)
    total_dataset = update_dataset([ids,usernames,tweets,favorites,retweets])
    scoreboard = get_scoreboard(total_dataset[1],total_dataset[3],total_dataset[4])

    for item in scoreboard:
        scoreboard[item]['ranking'] = get_rank(scoreboard[item]['points'])
    with open(filepath + 'scoreboard.json', 'w') as F:
        F.write(json.dumps(scoreboard))
    top_tweet([ids,tweets,usernames,favorites,retweets])

def get_scoreboard(usernames,favorites,retweets):
    username_points = {}

    for i in range(len(usernames)):

        if usernames[i] in username_points:
            username_points[usernames[i]] = {'tweets':username_points[usernames[i]]['tweets']+1,
                                        'likes':username_points[usernames[i]]['likes']+ favorites[i],
                                        'retweets':username_points[usernames[i]]['retweets']+ retweets[i],
                                        'points':username_points[usernames[i]]['points'] + min(MAX_POINTS,(TWEET_POINTS + favorites[i] * LIKE_POINTS + retweets[i] * RETWEET_POINTS))}
        else:
            username_points[usernames[i]]= {'tweets':1,
                                    'likes':favorites[i],
                                    'retweets':retweets[i],
                                    'points':min(MAX_POINTS,(TWEET_POINTS + favorites[i] * LIKE_POINTS + retweets[i] * RETWEET_POINTS))}

    sorted_keys = sorted(username_points,reverse=True, key=lambda x: (username_points[x]['points'], username_points[x]['tweets']))
    scoreboard = {}

    for key in sorted_keys:
        scoreboard[key] = username_points[key]

    return scoreboard

def get_rank(point):
    df = pd.read_csv(filepath +'ranking.csv')
    df = df[::-1]
    rankings = df['RANK'].tolist()
    points_needed = df['POINTS'].tolist()
    if point > 100:
        for i in range(0,len(points_needed)):
            if point > points_needed[i] :
                return str(rankings[i])
    return 'Villager'



main()


