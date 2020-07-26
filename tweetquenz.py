import json
import time
from argparse import ArgumentParser, FileType
from dataclasses import asdict
from datetime import datetime
from random import randrange
from typing import List, Optional, TextIO

from serial import Serial
from tweepy import OAuthHandler, Status, Stream, StreamListener
from urllib3.exceptions import HTTPError

from printer import Printer, print_tweet
from twitter_credentials import (
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET,
)
from utils import Tweet

PROGRAM_VERSION = "0.9.16e - Narcoleptic Night-snake"

TWITTER_KEYWORDS = [
    "@BurgWaldeck",
    "@WFreakquenz",
    "#digitalfreakquenz",
    "#waldeckfreakquenz",
    "freakquenz",
    "#twitterprinter",
]


class Listener(StreamListener):
    def __init__(
        self,
        printer: Printer,
        arduino: Optional[Serial] = None,
        rawfile: Optional[TextIO] = None,
        outfile: Optional[TextIO] = None,
    ):
        super().__init__()  # Initialize with default API
        self.arduino = arduino
        self.rawfile = rawfile
        self.outfile = outfile
        self.printer = printer

    def on_status(self, status: Status) -> None:
        """Processes a tweet, or as Twitter calls it, a "status"."""
        self.signal_arduino() # first, turn the lights on
        self.store_raw_status(status)
        tweet = Tweet.from_status(status)
        print(f"{datetime.now():%F %T} Printing tweet from {tweet.handle}")
        self.store_tweet(tweet)
        self.print_tweet(tweet)

    def on_error(self, status: int) -> None:
        print(f"Error when using Twitter: {status}")

    def print_tweet(self, tweet: Tweet) -> None:
        print_tweet(tweet, self.printer, indent=randrange(12))

    def signal_arduino(self) -> None:
        if self.arduino is not None:
            self.arduino.write(b"tweet!")

    def store_raw_status(self, status: Status) -> None:
        if self.rawfile is not None:
            json.dump(asdict(Status), self.rawfile)
            self.rawfile.write("\n")

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
        type=FileType("wb", bufsize=0),
    )
    parser.add_argument(
        "--encoding",
        default="cp437",
        help="Character set to use for the printer output (default: cp437)",
    )
    parser.add_argument(
        "--copy-to",
        help="Adds Tweets as JSON to this file, one per line",
        type=FileType("a", bufsize=1),
    )
    parser.add_argument(
        "--dump-raw-to",
        help="Dumps the raw Twitter-status to this file, one per line",
        type=FileType("a", bufsize=1),
    )
    parser.add_argument("--arduino", help="Serial port for external Arduino triggers.")
    parser.add_argument(
        "--baudrate",
        type=int,
        default=9600,
        help="Arduino serial baudrate (default: 9600)",
    )
    args = parser.parse_args()

    print(f"TwitterPrinter v{PROGRAM_VERSION}, reporting for duty!")

    if args.arduino is not None:
        arduino_serial = Serial(port=args.arduino, baudrate=args.baudrate)
        arduino_serial.write(b"Hello!")
    printer = Printer(args.printer, encoding=args.encoding)
    listener = Listener(printer, arduino=arduino_serial, outfile=args.copy_to, rawfile=args.dump_raw_to)
    while True:
        try:
            stream_tweets(listener, TWITTER_KEYWORDS)
        except HTTPError as exc:
            print(f"Something went wrong talking to twitter: {exc}")
            print("  We'll retry in just a second")
            time.sleep(1)  # Sometimes Twitter hangs up the phone, just retry


if __name__ == "__main__":
    main()
