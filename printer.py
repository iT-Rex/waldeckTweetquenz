from typing import BinaryIO

from utils import Tweet, character_encoder, reflow


class Printer:
    WIDE_MODE = "\x1bW%d"
    QUALITY_MODE = "\x1bx%d"
    EMPHASIZED_MODE = "\x1bE"
    NON_EMPHASIZED_MODE = "\x1bF"
    DOUBLE_STRIKE_MODE = "\x1bG"
    SINGLE_STRIKE_MODE = "\x1bH"
    EXTENDED_CHARACTER_MODE = "\x1b6"
    WEIGHTS = {
        "light": SINGLE_STRIKE_MODE + NON_EMPHASIZED_MODE,
        "normal": DOUBLE_STRIKE_MODE + NON_EMPHASIZED_MODE,
        "bold": DOUBLE_STRIKE_MODE + EMPHASIZED_MODE,
    }

    def __init__(
        self, device: BinaryIO, width: int = 1, encoding: str = "cp437", left_margin=0,
    ):
        self.device = device
        self.encoder = character_encoder(encoding)
        self._write(self.EXTENDED_CHARACTER_MODE)

    def feed(self, lines: int = 4) -> None:
        """Generates a blank area between printed blocks."""
        self._write("\n" * lines)

    def print(
        self,
        text: str,
        indent: int = 0,
        end: str = "\n",
        weight: str = "normal",
        wide: bool = False,
        nlq: bool = True,
    ) -> None:
        """Takes an input string and prints it, terminating with a newline.

        Indentation can be controlled using `indent` as a number of spaces.
        Alternate termination can be achieved by providing an `end` string.
        Weight is controlled by providing one of 'light', 'normal' or 'bold'.
        Double-wide printing and 'near-letter-quality' are controlled using
        the `wide` and `nlq` parameters respectively.
        """
        if indent:
            self._write(self.WIDE_MODE % 1)
            self._write(" " * indent)
        self._write(self.WEIGHTS[weight])
        self._write(self.WIDE_MODE % int(wide))
        self._write(self.QUALITY_MODE % int(nlq))
        self._write(text + end)
        # Switch NLQ light on, because it's like that on the CD Cover ;)
        self._write(self.QUALITY_MODE % 1)

    def _write(self, text: str) -> None:
        out_bytes = b"".join(map(self.encoder, text))
        self.device.write(out_bytes)


def print_tweet(tweet: Tweet, printer: Printer, indent: int = 0) -> None:
    """Takes a printer and a tweet and prints a nicely laid out block."""
    printer.print(tweet.author, indent=indent, weight="bold", end=" ")
    printer.print(f"({tweet.handle})", end=" ", weight="light")
    printer.print(f" · {tweet.created_at}", end="\n\n", weight="light", nlq=False)
    for line in reflow(tweet.text):
        printer.print(line, indent=indent, weight="bold", wide=True)
    if tweet.source:
        printer.print(f" ── Sent from {tweet.source}", indent=indent, nlq=False)
    printer.feed()
