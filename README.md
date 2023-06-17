

get last 100 tweets, mentions and replies of a specific user

> all user's mentions will be published to the `user_mentions` channel using redis pubsub.

> all user's replies will be published to the `user_replies` channel using redis pubsub.

> all user's tweets will be published to the `user_tweets` channel using redis pubsub.


## 🚀 Deploy

> Make sure that you've setup your twitter keys and redis address, username and password inside the `main.py`

```bash
sudo chmod +x redeploy.sh && ./redeploy.sh
```