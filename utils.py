from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from textwrap import wrap
from typing import Callable, Dict, Iterator, List, Optional

from tweepy import Status

SPECIAL_CHARACTERS = {"€": "C\b="}
TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"
WEEKDAYS = (
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
)
MONTHS = (
    None,
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
)


@dataclass
class Tweet:
    """A greatly simplified view of a Tweet, for simpler people."""

    text: str
    tags: List[str]
    author: str
    handle: str
    source: Optional[str]
    created_at: str

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
            source=status.source,
            created_at=cls._format_datetime(status.created_at),
        )

    @classmethod
    def _format_datetime(cls, dtime: datetime) -> str:
        """Parses datetime from tweet and formats it for a German locale."""
        weekday = WEEKDAYS[dtime.weekday()]
        month = MONTHS[dtime.month]
        return f"{weekday}, {dtime.day}. {month} {dtime.year}, {dtime:%H:%M}"

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
