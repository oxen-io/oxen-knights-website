# Oxen Knights

Oxen Knights dashboard

# Requirements

`pip install django python-dotenv pandas tweepy==3.10.0`

# Setup

## Set tweepy api key

Set twitter api key in updatedata.py

```
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
```

## Generate index.html and ranking reward.html

`python updatedata.py updaterank.py`

## Run Django server

`python manage.py runserver`

## Updating scoreboard

`python updatedata.py`
