from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import twitter_credentials

class StdOutListener(StreamListener):

	def on_data(self, data):
		jsonData = json.loads(data)
		print(jsonData['text'])
		return True

	def on_error(self, status):
		print(status)

if __name__ == "__main__":
	listener = StdOutListener()
	auth = OAuthHandler(twitter_credentials.API_KEY, twitter_credentials.API_SECRET_KEY)
	auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
	filterStringList = ["nintendo"]

	stream = Stream(auth, listener)

	stream.filter(track = filterStringList)
