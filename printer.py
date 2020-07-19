from itertools import repeat


class Printer:
    WIDE_MODE = "\x1bW{width}"
    QUALITY_MODE = "\x1bx{quality}"

    def __init__(self, device="/dev/lp0", width=1, quality=1):
        self.device = device
        self._send(self.WIDE_MODE.format(width=width))
        self._send(self.QUALITY_MODE.format(quality=quality))

    def print(self, line, weight=2):
        """Takes an input string and prints it, terminating with a newline.

        This also implements a printing `weight` that's achieved using a simple
        carriage return and reprint. For this to work, the given line must not
        contain its own newlines.
        """
        for data in repeat(line, weight):
            self._send(data + "\r")
        self._send("\n")

    def separator(self):
        """Generates a big blank separator between printed blocks."""
        self._send("\n" * 6)

    def _send(self, raw):
        with open(self.device, "w") as fp:
            fp.write(raw)
