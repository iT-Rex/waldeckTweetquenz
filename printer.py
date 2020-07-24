from enum import Enum, auto
from typing import BinaryIO, Set

from utils import Tweet, character_encoder, reflow


class Mode(Enum):
    double_strike = auto()
    emphasized = auto()
    nlq = auto()
    wide = auto()


class Style(Enum):
    author = {Mode.double_strike, Mode.emphasized, Mode.nlq}
    handle = {Mode.emphasized, Mode.nlq}
    separator = {Mode.double_strike, Mode.emphasized}
    timestamp = {Mode.emphasized}
    body = {Mode.double_strike, Mode.emphasized, Mode.nlq, Mode.wide}
    footer: Set[Mode] = set()


class Printer:
    WIDE_TOGGLE = "\x1bW0", "\x1bW1"
    NLQ_TOGGLE = "\x1bx0", "\x1bx1"
    EMPHASIZED_TOGGLE = "\x1bE", "\x1bF"
    DOUBLE_STRIKE_TOGGLE = "\x1bG", "\x1bH"
    EXTENDED_CHARACTER_MODE = "\x1b6"

    def __init__(self, device: BinaryIO, encoding: str = "cp437"):
        self.device = device
        self.encoder = character_encoder(encoding)
        self._write(self.EXTENDED_CHARACTER_MODE)

    def feed(self, lines: int = 4) -> None:
        """Generates a blank area between printed blocks."""
        self._write("\n" * lines)

    def print(self, text: str, style: Style, indent: int = 0, end: str = "\n") -> None:
        """Takes an input string and prints it, terminating with a newline.

        Indentation can be controlled using `indent` as a number of spaces.
        Alternate termination can be achieved by providing an `end` string.
        Style is controlled by passing a Style enum, whose values are a set
        of Mode parameters, understood by the Printer.
        """
        if indent:
            self._write(self.WIDE_TOGGLE[False])
            self._write(" " * indent)
        self._set_modes(style.value)
        self._write(text + end)
        # Switch NLQ light on, because it's like that on the CD Cover ;)
        self._write(self.NLQ_TOGGLE[True])

    def _set_modes(self, modes: Set[Mode]):
        """Sends mode toggles based on their enabled state in the given set."""
        self._write(self.WIDE_TOGGLE[Mode.wide in modes])
        self._write(self.NLQ_TOGGLE[Mode.nlq in modes])
        self._write(self.EMPHASIZED_TOGGLE[Mode.emphasized in modes])
        self._write(self.DOUBLE_STRIKE_TOGGLE[Mode.double_strike in modes])

    def _write(self, text: str) -> None:
        out_bytes = b"".join(map(self.encoder, text))
        self.device.write(out_bytes)


def print_tweet(tweet: Tweet, printer: Printer, indent: int = 0) -> None:
    """Takes a printer and a tweet and prints a nicely laid out block."""
    printer.print(tweet.author, Style.author, indent=indent, end=" ")
    printer.print(f"({tweet.handle})", Style.handle, end=" ")
    printer.print("·", Style.separator, end=" ")
    printer.print(tweet.created_at, Style.timestamp, end="\n\n")
    for line in reflow(tweet.text):
        printer.print(line, Style.body, indent=indent)
    if tweet.source:
        printer.print(f" ── Sent from {tweet.source}", Style.footer, indent=indent)
    printer.feed()
