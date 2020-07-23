import json
import time
from argparse import ArgumentParser, FileType
from dataclasses import asdict
from http.client import HTTPException
from typing import List, Optional, TextIO

from tweepy import OAuthHandler, Status, Stream, StreamListener

from printer import Printer
from twitter_credentials import (
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)
from utils import Tweet, reflow

TWITTER_KEYWORDS = [
    "@BurgWaldeck",
    "@WFreakquenz",
    "#digitalfreakquenz",
    "#waldeckfreakquenz",
    "freakquenz",
]


class Listener(StreamListener):
    def __init__(self, printer: Printer, outfile: Optional[TextIO] = None):
        super().__init__()  # Initialize with default API
        self.outfile = outfile
        self.printer = printer

    def on_status(self, status: Status) -> None:
        """Processes a tweet, or as Twitter calls it, a "status"."""
        tweet = Tweet.from_status(status)
        print(f"{status.created_at:%H:%M:%S} Printing tweet from {tweet.handle}")
        self.print_tweet(tweet)
        self.store_tweet(tweet)

    def on_error(self, status: int) -> None:
        print(f"Error when using Twitter: {status}")

    def print_tweet(self, tweet: Tweet) -> None:
        for line in reflow(tweet.text):
            self.printer.print(line)
        self.printer.separator()

    def store_tweet(self, tweet: Tweet) -> None:
        if self.outfile is not None:
            json.dump(asdict(tweet), self.outfile)
            self.outfile.write("\n")


def stream_tweets(listener: Listener, hash_tag_list: List[str]) -> None:
    auth = OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=hash_tag_list)


def main() -> None:
    parser = ArgumentParser(description="Prints tweets to a line printer.")
    parser.add_argument(
        "--printer",
        default="/dev/lp0",
        help="Path to the printer device to use (default: /dev/lp0)",
        type=FileType("wb"),
    )
    parser.add_argument(
        "--encoding",
        default="cp850",
        help="Character set to use for the printer output (default: cp850)",
    )
    parser.add_argument(
        "--copy-to",
        help="Adds Tweets as JSON to this file, one per line",
        type=FileType("a"),
    )
    args = parser.parse_args()

    printer = Printer(args.printer, encoding=args.encoding)
    listener = Listener(printer, outfile=args.copy_to)
    while True:
        try:
            stream_tweets(listener, TWITTER_KEYWORDS)
        except HTTPException as exc:
            print(f"Something went wrong talking to twitter: {exc}")
            print("  We'll retry in just a second")
            time.sleep(1)  # Sometimes Twitter hangs up the phone, just retry


if __name__ == "__main__":
    main()
