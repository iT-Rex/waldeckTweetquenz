import json
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from printer import Printer
from twitter_credentials import (
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)
from utils import reflow

TWITTER_KEYWORDS = [
    "@BurgWaldeck",
    "@WFreakquenz",
    "#digitalfreakquenz",
    "#waldeckfreakquenz",
    "freakquenz",
]


class Listener(StreamListener):
    def __init__(self, printer: Printer):
        self.printer = printer

    def on_data(self, data):
        tweet = json.loads(data)
        for line in reflow(tweet["text"]):
            self.printer.print(line)
        self.printer.separator()
        return True

    def on_error(self, status):
        print(status)


def tweet_streamer(printer, hash_tag_list):
    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, Listener(printer))
    stream.filter(track=hash_tag_list)


def main(printer_path: str = "/dev/lp0"):
    with open(printer_path, "wb") as printer_fp:
        printer = Printer(printer_fp)
        tweet_streamer(printer, TWITTER_KEYWORDS)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
