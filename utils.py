from __future__ import annotations

from dataclasses import dataclass
from textwrap import wrap
from typing import Callable, Dict, Iterator, List

from tweepy import Status

SPECIAL_CHARACTERS = {"€": "C\b="}


@dataclass
class Tweet:
    """A greatly simplified view of a Tweet, for simpler people."""

    text: str
    tags: List[str]
    author: str
    handle: str

    @classmethod
    def from_status(cls, status: Status) -> Tweet:
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
            tags = cls._get_tags(status.extended_tweet["entities"]["hashtags"])
        else:
            text = status.text
            tags = cls._get_tags(status.entities["hashtags"])
        return cls(
            text=text,
            tags=list(tags),
            author=status.user.name,
            handle=f"@{status.user.screen_name}",
        )

    @classmethod
    def _get_tags(cls, tags: List[Dict[str, str]]):
        for tag in tags:
            yield f"#{tag['text']}"


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
