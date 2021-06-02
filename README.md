# Oxen Knights
Oxen Knights dashboard

# Requirements
```pip install pandas tweepy```

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
```python updatedata.py```
```python updaterank.py```

## Run Django server
```python manage.py runserver```

## Updating scoreboard
```python updatedata.py```
