"""Text normalization and character utilities."""

from __future__ import annotations
import unicodedata
import re
from typing import Dict
from writegenius.nlp.stopwords import STOPWORDS_BY_LANG

# Mapping for specific Slavic/Polish characters if standard NFD decomposition differs
SPECIAL_DIACRITICS_MAP = {
    "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ź": "z", "ż": "z",
    "Ą": "A", "Ć": "C", "Ę": "E", "Ł": "L", "Ń": "N", "Ó": "O", "Ś": "S", "Ź": "Z", "Ż": "Z",
}


def strip_diacritics(text: str) -> str:
    """Remove diacritics and accents from characters.

    Args:
        text: Input string with diacritics (e.g., 'Zażółć gęślą jaźń').

    Returns:
        ASCII-normalized representation ('Zazolc gesla jazn').
    """
    if not text:
        return ""

    # Replace specific characters like Polish 'ł'/'Ł' which aren't decomposed by standard NFD
    res = []
    for ch in text:
        if ch in SPECIAL_DIACRITICS_MAP:
            res.append(SPECIAL_DIACRITICS_MAP[ch])
        else:
            res.append(ch)
    intermediate = "".join(res)

    # Decompose Unicode characters and filter out combining marks
    nfkd = unicodedata.normalize("NFKD", intermediate)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_whitespace(text: str) -> str:
    """Normalize multiple spaces, tabs, and newlines into single spaces."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def clean_text(
    text: str,
    remove_diacritics: bool = False,
    lowercase: bool = True,
    preserve_sentences: bool = True,
) -> str:
    """Standardize text for NLP processing.

    Args:
        text: Input raw string.
        remove_diacritics: If True, strips language accents.
        lowercase: If True, converts all characters to lowercase.
        preserve_sentences: If False, strips all punctuation.

    Returns:
        Cleaned text string.
    """
    if not text:
        return ""

    output = text
    if remove_diacritics:
        output = strip_diacritics(output)

    if lowercase:
        output = output.lower()

    if not preserve_sentences:
        output = re.sub(r"[^\w\s]", "", output, flags=re.UNICODE)

    return normalize_whitespace(output)


def detect_language_heuristic(text: str) -> str:
    """Fast, lightweight rule-and-stopword heuristic to detect European language.

    Supports: 'pl', 'en', 'de', 'fr', 'es'.

    Args:
        text: Input text string.

    Returns:
        ISO 639-1 language code (defaults to 'pl' if Polish characters detected, else 'en').
    """
    if not text:
        return "en"

    # Specific distinctive Polish letters
    pl_unique = set("ąćęłńśźżĄĆĘŁŃŚŹŻ")
    if any(c in pl_unique for c in text):
        return "pl"

    de_unique = set("äöüßÄÖÜ")
    if any(c in de_unique for c in text):
        return "de"

    # Tokenize words in lowercase
    words = [w.lower() for w in re.findall(r"\b\w+\b", text)]
    if not words:
        return "en"

    scores: Dict[str, int] = {}
    for lang, stops in STOPWORDS_BY_LANG.items():
        overlap = sum(1 for w in words if w in stops)
        scores[lang] = overlap

    best_lang = max(scores, key=scores.get) # type: ignore
    # If no stopwords matched at all, default to 'en'
    if scores[best_lang] == 0:
        return "en"

    return best_lang
