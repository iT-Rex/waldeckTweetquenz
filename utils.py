from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from textwrap import wrap
from typing import Callable, Dict, Iterator, List, Optional

from tweepy import Status

SPECIAL_CHARACTERS = {
    "cp437": {
        "…": "_",
        "€": "ε",
        "₤": "£",
        "’": "'",
        "‘": "'",
        "‚": "'",
        "„": '"',
        "“": '"',
        "”": '"',
        "‹": "«",
        "›": "»",
        "☺": "\x01",
        "☻": "\x02",
        "♥": "\x03",
        "♦": "\x04",
        "♣": "\x05",
        "♠": "\x06",
        "❤": "\x03",
    }
}
EMOJI = re.compile(r"[\U0001F300-\U0001FADF]")
TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"
WEEKDAYS_SHORT = "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"
MONTHS_SHORT = (
    None,
    "Jan.",
    "Feb.",
    "März",
    "Apr.",
    "Mai",
    "Juni",
    "Juli",
    "Aug.",
    "Sept.",
    "Okt.",
    "Nov.",
    "Dez.",
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
        weekday = WEEKDAYS_SHORT[dtime.weekday()]
        month = MONTHS_SHORT[dtime.month]
        return f"{weekday}, {dtime.day}. {month} {dtime.year}, {dtime:%H:%M}"

    @classmethod
    def _get_tags(cls, tags: List[Dict[str, str]]):
        for tag in tags:
            yield f"#{tag['text']}"


def character_encoder(encoding: str) -> Callable[[str], bytes]:
    substitution_map = SPECIAL_CHARACTERS.get(encoding, {})

    def _encoder(character: str) -> bytes:
        try:
            if (substitution := substitution_map.get(character)) is not None:
                return substitution.encode(encoding)
            if EMOJI.match(character):
                return "■".encode(encoding)
            return character.encode(encoding)
        except UnicodeEncodeError:
            return b"\x04"  # encoding result of last resort

    return _encoder


def reflow(text: str, line_length: int = 30) -> Iterator[str]:
    for paragraph in text.split("\n"):
        yield from wrap(paragraph, width=line_length)
