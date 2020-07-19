import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
from printer import Printer
from utils import reflow


class TwitterStreamer():
  def stream_tweets(self, hash_tag_list):
    listener = StdOutListener()
    auth = OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)
    stream.filter(track = hash_tag_list)

class StdOutListener(StreamListener):
  def on_data(self, data):
    jsonData = json.loads(data)
    tweetText = jsonData['text']

    printer = Printer()
    for line in reflow(tweetText):
      printer.print(line)
    printer.separator()

    return True

  def on_error(self, status):
    print(status)

if __name__ == "__main__":
  hash_tag_list = ['@BurgWaldeck','#waldeckfreakquenz','@WFreakquenz','#digitalfreakquenz','freakquenz']

  twitterStreamer = TwitterStreamer()
  twitterStreamer.stream_tweets(hash_tag_list)
