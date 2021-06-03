import tweepy as tw
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import csv
import pandas as pd
import json
from collections import OrderedDict
import datetime as DT

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_term = "$oxen -filter:retweets"

raw_data = tw.Cursor(api.search,
                   q=search_term,
                   lang="en",
                   since=str(DT.date.today()- DT.timedelta(days=7))).items(5000)

TWEET_POINTS = 10
LIKE_POINTS = 1
RETWEET_POINTS = 5
MAX_POINTS = 150

## Take in new scraped data and add it to json file
def update_dataset(data):
    json_file =[[],[],[],[],[]]
    try:
        with open('data.json', 'r') as F:
            json_file = json.loads(F.read())
    except:
        for i in range(0,len(data[0])):
            if data[0][i] not in json_file[0]:
                json_file[0].append(data[0][i])
                json_file[1].append(data[1][i])
                json_file[2].append(data[2][i])
                json_file[3].append(data[3][i])
                json_file[4].append(data[4][i])

    with open('data.json', 'w') as F:
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

    total_table(scoreboard)

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
    df = pd.read_csv('ranking.csv')
    df = df[::-1]
    rankings = df['RANK'].tolist()
    points_needed = df['POINTS'].tolist()
    if point > 100:
        for i in range(0,len(points_needed)):
            if point > points_needed[i] :
                return str(rankings[i])
    return 'Peasant'

def total_table(scoreboard):
        
    start_html = """
    <script>
    $(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();
</script>
    {% extends 'base.html' %}
    {% block body %}
    <html><head>
    <meta charset="UTF-8">
    </head>
 
    <body>

    <div class="container">
    <center>
    <img width="350px" class="pbot20" src="static/assets/OXEN_BRAND_PRIMARY.png"><br>
    <h1 class="pbot10">Knight Scoreboard</h1></center>
    <div class="tbl-header">
        <table cellpadding="0" cellspacing="0" border="0">
            <thead>
                <th><font class="column_name">Twitter Handle</font></th>
                <th><font class="column_name">Ranking</font></th>
                <th><font class="column_name">Points</font></th>
                <th><font class="column_name">Tweets</font></th>
                <th><font class="column_name">Likes</font></th>
                <th><font class="column_name">Retweets</font></th>
            </thread>
        </table>
    </div>
    <div class="tbl-content">
        <table cellpadding="0" cellspacing="0" border="0">
            <tbody>
                <tr>
    """
    end_html = "</tbody></table></div></body></html>{% endblock %}"

    for item in scoreboard.items():
        start_html += f"""<tr>
        <td> <a href="https://twitter.com/{item[0]}">@{item[0]}</a></th>
        <td><img style="width:30px" src ="static/assets/{item[1]['ranking'].lower()}.svg"> {item[1]['ranking']}</th>
        <td>{item[1]['points']}</td>
        <td>{item[1]['tweets']}</td>
        <td>{item[1]['likes']}</td>
        <td>{item[1]['retweets']}</td>
        </tr>
        """

    start_html += end_html
    f = open('scoreboard/templates/index.html','w', encoding="utf-8")
    f.write(start_html)
    f.close()

    
main()


