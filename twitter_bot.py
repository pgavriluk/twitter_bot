import tweepy
import time

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

user = api.me()
print(user.description)


def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        time.sleep(1000)
    except StopIteration:
        return


for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    print(follower.name)

search_string = 'python'
number_of_tweets = 2

for tweet in limit_handler(tweepy.Cursor(api.search, search_string).items(number_of_tweets)):
    try:
        print(tweet)
        tweet.favorite()
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
