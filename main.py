

from fastapi import FastAPI
import tweepy
from datetime import datetime
import redis
import time
import json 

app = FastAPI()

red = redis.StrictRedis('redis', 6379, password="" , charset="utf-8", decode_responses=True)

client_id = ""
client_secret = ""
bearer_token = ""
access_token = ""
access_token_secret = ""
api_secret = ""
api_key = ""


client = tweepy.Client(
    bearer_token, 
    api_key, 
    api_secret, 
    access_token, 
    access_token_secret
)

@app.get("/get-user-tweets/{username}")
def get_latest_tweets(username: str, count: int = 3000):
    try:
        account = client.get_user(username=username).data.id
        tweets = client.get_users_tweets(account, max_results=count, exclude='replies').data
        latest_tweets = []
        for tweet in tweets:
            latest_tweets.append({"text": tweet.text, "created_at": tweet.created_at})
        now = datetime.now()
        print("request handled in [get-user-tweets] route at time ", now.strftime("%Y,%M%D - %H:%M:%S"))

        red.publish('user_tweets', json.dumps(latest_tweets))
        
        return {"username": username, "tweets": latest_tweets}
    except tweepy.errors.TweepyException as e:
        return {"error": str(e)}
    
    
@app.get("/get-user-mentions/{username}")
def get_latest_tweets(username: str, count: int = 3000):
    try:
        account = client.get_user(username=username).data.id
        mentions = client.get_users_mentions(account, max_results=count, expansions=['author_id']).data
        latest_mentions = []
        for mention in mentions:
            latest_mentions.append({"text": mention.text, "created_at": mention.created_at})
        now = datetime.now()
        print("request handled in [get-user-mentions] route at time ", now.strftime("%Y,%M%D - %H:%M:%S"))
            
        red.publish('user_mentions', json.dumps(latest_mentions))
        
        return {"username": username, "mentions": latest_mentions}
    except tweepy.errors.TweepyException as e:
        return {"error": str(e)}
    
    
@app.get("/get-user-replies/{username}")
def get_latest_replies(username: str, count: int = 3000):
    try:
        account = client.get_user(username=username).data.id
        tweets = client.get_users_tweets(account, max_results=count).data
        latest_tweets = []
        for tweet in tweets:
            tweet_id = tweet.id
            latest_tweets.append({"text": tweet.text, "created_at": tweet.created_at})
        now = datetime.now()
        print("request handled in [get-user-replies] route at time ", now.strftime("%Y,%M%D - %H:%M:%S"))
        
        red.publish('user_replies', json.dumps(latest_tweets))
        
        return {"username": username, "tweets": latest_tweets}
    except tweepy.errors.TweepyException as e:
        return {"error": str(e)}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
