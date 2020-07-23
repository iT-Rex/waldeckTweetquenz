from typing import BinaryIO

from utils import Tweet, character_encoder, reflow


class Printer:
    WIDE_MODE = "\x1bW%d"
    QUALITY_MODE = "\x1bx%d"
    EMPHASIZED_MODE = "\x1bE"
    NON_EMPHASIZED_MODE = "\x1bF"
    DOUBLE_STRIKE_MODE = "\x1bG"
    EXTENDED_CHARACTER_MODE = "\x1b6"
    LEFT_MARGIN_MODE = "\x1b\x6c"

    def __init__(
        self, device: BinaryIO, width: int = 1, encoding: str = "cp437",
    ):
        self.device = device
        self.encoder = character_encoder(encoding)
        self._write(self.QUALITY_MODE % 1)
        self._write(self.DOUBLE_STRIKE_MODE)
        self._write(self.EXTENDED_CHARACTER_MODE)

    def feed(self, lines: int = 4) -> None:
        """Generates a blank area between printed blocks."""
        self._write("\n" * lines)

    def left_margin(self, margin: int) -> None:
        """Sets the default left margin, allowing it to be funky."""
        self._write(self.LEFT_MARGIN_MODE + chr(margin))

    def print(
        self, text: str, end: str = "\n", bold: bool = False, wide: bool = False
    ) -> None:
        """Takes an input string and prints it, terminating with a newline.

        If newline termination is not desired, an alternative `end` string can
        be provided.

        The `bold` parameter controls Emphasized printing, wheras the `wide`
        parameter controls double-width mode.
        """
        self._write(self.EMPHASIZED_MODE if bold else self.NON_EMPHASIZED_MODE)
        self._write(self.WIDE_MODE % int(wide))
        self._write(text + end)

    def _write(self, text: str) -> None:
        out_bytes = b"".join(map(self.encoder, text))
        self.device.write(out_bytes)


def print_tweet(tweet: Tweet, printer: Printer, left_margin: int = 0) -> None:
    """Takes a printer and a tweet and prints a nicely laid out block."""
    printer.left_margin(left_margin)
    printer.print(tweet.author, bold=True, end=" ")
    printer.print(f"({tweet.handle})", end=" ")
    printer.print(f" · {tweet.created_at}", end="\n\n")
    for line in reflow(tweet.text):
        printer.print(line, wide=True, bold=True)
    if tweet.source:
        printer.print("── Sent from {tweet.source}")
    printer.feed()
