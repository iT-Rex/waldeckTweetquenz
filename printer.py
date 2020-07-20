from itertools import repeat

from utils import character_encoder


class Printer:
    WIDE_MODE = b"\x1bW%d"
    QUALITY_MODE = b"\x1bx%d"

    def __init__(
        self,
        device: str = "/dev/lp0",
        width: int = 1,
        quality: int = 1,
        encoding: str = "cp850",
    ):
        self.device = device
        self.encoding = encoding
        self._write(self.WIDE_MODE % width)
        self._write(self.QUALITY_MODE % quality)

    def print(self, text: str, weight: int = 2) -> None:
        """Takes an input string and prints it, terminating with a newline.

        This also implements a printing `weight` that's achieved using a simple
        carriage return and reprint. For this to work, the given line must not
        contain its own newlines.
        """
        for data in repeat(self._encoder(text + "\r"), weight):
            self._write(data)
        self._write(b"\n")

    def separator(self) -> None:
        """Generates a big blank separator between printed blocks."""
        self._write(b"\n" * 6)

    def _encoder(self, text: str) -> bytes:
        encoder = character_encoder(self.encoding)
        return b"".join(map(encoder, text))

    def _write(self, raw: bytes) -> None:
        with open(self.device, "wb") as fp:
            fp.write(raw)
