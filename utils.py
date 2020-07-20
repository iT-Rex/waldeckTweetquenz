from textwrap import wrap
from typing import Callable, Iterator

SPECIAL_CHARACTERS = {"€": "C\b="}


def character_encoder(encoding: str) -> Callable[[str], bytes]:
    def _encoder(character: str) -> bytes:
        if character in SPECIAL_CHARACTERS:
            return SPECIAL_CHARACTERS[character].encode(encoding)
        try:
            return character.encode(encoding)
        except UnicodeEncodeError:
            return "?".encode(encoding)

    return _encoder


def reflow(text: str, line_length: int = 30) -> Iterator[str]:
    for paragraph in text.split("\n"):
        yield from wrap(paragraph, width=line_length)
