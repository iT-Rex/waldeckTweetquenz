from typing import BinaryIO

from utils import character_encoder


class Printer:
    WIDE_MODE = "\x1bW%d"
    QUALITY_MODE = "\x1bx%d"
    EMPHASIZED_MODE = "\x1bE"
    DOUBLE_STRIKE_MODE = "\x1bG"

    def __init__(
        self,
        device: BinaryIO,
        width: int = 1,
        high_quality: bool = True,
        encoding: str = "cp850",
    ):
        self.device = device
        self.encoder = character_encoder(encoding)
        if high_quality:
            self._write(self.QUALITY_MODE % 1)
            self._write(self.EMPHASIZED_MODE)
            self._write(self.DOUBLE_STRIKE_MODE)
        self._write(self.WIDE_MODE % width)

    def print(self, text: str) -> None:
        """Takes an input string and prints it, terminating with a newline."""
        self._write(text + "\n")

    def separator(self) -> None:
        """Generates a big blank separator between printed blocks."""
        self._write("\n" * 6)

    def _write(self, text: str) -> None:
        out_bytes = b"".join(map(self.encoder, text))
        self.device.write(out_bytes)
