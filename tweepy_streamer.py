from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import twitter_credentials

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
		print(jsonData['text'])
		return True

	def on_error(self, status):
		print(status)

if __name__ == "__main__":
	hash_tag_list = ['nintendo']
	
	twitterStreamer = TwitterStreamer()
	twitterStreamer.stream_tweets(hash_tag_list)
