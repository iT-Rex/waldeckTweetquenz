from utils import character_encoder


class Printer:
    WIDE_MODE = "\x1bW%d"
    QUALITY_MODE = "\x1bx%d"
    EMPHASIZED_MODE = "\x1bE"
    DOUBLE_STRIKE_MODE = "\x1bG"

    def __init__(
        self,
        device: str = "/dev/lp0",
        width: int = 1,
        high_quality: bool = True,
        encoding: str = "cp850",
    ):
        self.device = device
        self.encoding = encoding
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

    def _encode(self, text: str) -> bytes:
        encoder = character_encoder(self.encoding)
        return b"".join(map(encoder, text))

    def _write(self, text: str) -> None:
        with open(self.device, "wb") as fp:
            fp.write(self._encode(text))
