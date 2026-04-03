from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher


STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "of",
    "for",
    "in",
    "on",
    "to",
    "with",
    "world",
    "results",
}

FORMAT_ALIASES = {
    "paperback": "paperback",
    "paper back": "paperback",
    "pb": "paperback",
    "hardcover": "hardcover",
    "hard cover": "hardcover",
    "hc": "hardcover",
}

EDITION_ALIASES = {
    "1st paperback edition": "paperback",
    "paperback": "paperback",
    "hardcover": "hardcover",
    "hard cover": "hardcover",
    "hardcover special edition": "hardcover",
}


def normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(value: str) -> list[str]:
    return [token for token in normalize_text(value).split() if token and token not in STOPWORDS]


def normalize_isbn(value: str) -> str:
    return re.sub(r"[^0-9xX]", "", value or "").upper()


def normalize_format(value: str) -> str:
    normalized = normalize_text(value)
    return FORMAT_ALIASES.get(normalized, normalized)


def normalize_edition(value: str) -> str:
    normalized = normalize_text(value)
    return EDITION_ALIASES.get(normalized, normalized)


def similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def token_overlap(left: str, right: str) -> float:
    left_tokens = set(tokenize(left))
    right_tokens = set(tokenize(right))
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
