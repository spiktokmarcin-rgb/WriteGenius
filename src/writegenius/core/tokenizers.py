"""Tokenization and syllabification utilities for European languages."""

from __future__ import annotations
import re
from typing import List, Tuple

# Common European vowel sets
POLISH_VOWELS = set("aąeęioóuyAĄEĘIOÓUY")
ENGLISH_VOWELS = set("aeiouyAEIOUY")
GERMAN_VOWELS = set("aeiouyäöüAEIOUYÄÖÜ")
FRENCH_VOWELS = set("aeiouyàâéèêëîïôùûüÿœæAEIOUYÀÂÉÈÊËÎÏÔÙÛÜŸŒÆ")
SPANISH_VOWELS = set("aeiouyáéíóúüAEIOUYÁÉÍÓÚÜ")

LANG_VOWEL_MAP = {
    "pl": POLISH_VOWELS,
    "en": ENGLISH_VOWELS,
    "de": GERMAN_VOWELS,
    "fr": FRENCH_VOWELS,
    "es": SPANISH_VOWELS,
    "it": set("aeiouàèéìíîòóùúAEIOUÀÈÉÌÍÎÒÓÙÚ"),
    "uk": set("аеєиіїоуюяАЕЄИІЇОУЮЯ"),
}


def tokenize_sentences(text: str) -> List[str]:
    """Split text into sentences, handling abbreviations and punctuation.

    Args:
        text: Input string.

    Returns:
        List of non-empty sentence strings.
    """
    if not text or not text.strip():
        return []

    # Regex handling common abbreviations (np., m.in., tzn., e.g., i.e., dr, etc.)
    # Protect common periods before splitting
    protected = text
    abbrevs = [
        r"\bnp\.",
        r"\bm\.in\.",
        r"\btzn\.",
        r"\btzw\.",
        r"\bul\.",
        r"\bdr\.",
        r"\bprof\.",
        r"\bi\.e\.",
        r"\be\.g\.",
        r"\betc\.",
    ]
    substitutions: list[tuple[str, str]] = []
    for i, pattern in enumerate(abbrevs):
        marker = f"__ABBR_{i}__"
        matches = re.findall(pattern, protected, flags=re.IGNORECASE)
        for m in set(matches):
            protected = protected.replace(m, marker)
            substitutions.append((marker, m))

    # Sentence boundary: [.!?]+ followed by space or newline
    raw_sentences = re.split(r"(?<=[.!?])\s+", protected)

    # Restore abbreviations
    sentences: List[str] = []
    for s in raw_sentences:
        restored = s.strip()
        for marker, original in substitutions:
            restored = restored.replace(marker, original)
        if restored:
            sentences.append(restored)

    return sentences


def tokenize_words(text: str, remove_punct: bool = True) -> List[str]:
    """Tokenize text into words.

    Args:
        text: Input string.
        remove_punct: If True, strips punctuation characters.

    Returns:
        List of token strings.
    """
    if not text:
        return []

    if remove_punct:
        # Match alphanumeric characters including Unicode letters (Polish, German, etc.)
        tokens = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
        # Filter out purely numeric or hyphen tokens if empty
        return [t for t in tokens if any(c.isalpha() for c in t)]
    else:
        return text.split()


def count_syllables_polish(word: str) -> int:
    """Accurately count syllables in a Polish word.

    In Polish, each vowel sound constitutes a syllable nucleus.
    However, the letter 'i' immediately followed by another vowel (ia, ie, io, iu, ią, ię)
    functions as a softening consonant / palatal glide, not an independent syllable nucleus.

    Args:
        word: A single Polish word.

    Returns:
        Integer count of syllables (minimum 1 for any non-empty word).
    """
    cleaned = re.sub(r"[^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", "", word.lower())
    if not cleaned:
        return 0

    # Polish vowels
    vowels = "aąeęioóuy"

    # Rule: Replace 'i' + vowel with single vowel indicator (glide softening)
    # e.g., 'nie-bo' -> 'ne-bo' (2 syllables), 'zro-bić' -> 'zro-bić' (2 syllables)
    glide_pattern = r"i([aąeęoóuy])"
    condensed = re.sub(glide_pattern, r"\1", cleaned)

    # Count remaining vowels
    count = sum(1 for char in condensed if char in vowels)
    return max(1, count)


def count_syllables_generic(word: str, lang: str = "en") -> int:
    """Count syllables for non-Polish European languages using vowel-cluster heuristics.

    Args:
        word: A single word.
        lang: ISO 639-1 language code ('en', 'de', 'fr', 'es', etc.).

    Returns:
        Integer count of syllables.
    """
    cleaned = re.sub(r"[^\w]", "", word.lower())
    if not cleaned:
        return 0

    vowels = LANG_VOWEL_MAP.get(lang, ENGLISH_VOWELS)

    # Count vowel groups
    count = 0
    in_vowel_group = False
    for char in cleaned:
        if char in vowels:
            if not in_vowel_group:
                count += 1
                in_vowel_group = True
        else:
            in_vowel_group = False

    # English-specific silent 'e' rule
    if lang == "en" and cleaned.endswith("e") and not cleaned.endswith("le") and count > 1:
        count -= 1

    return max(1, count)


def count_syllables(word: str, lang: str = "pl") -> int:
    """Count syllables in a word with language-specific rules.

    Args:
        word: A single word.
        lang: ISO language code (default: 'pl').

    Returns:
        Number of syllables.
    """
    if lang == "pl":
        return count_syllables_polish(word)
    return count_syllables_generic(word, lang=lang)


def extract_ngrams(words: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    """Extract n-grams from a list of tokens.

    Args:
        words: List of word tokens.
        n: Length of n-gram (e.g. 2 for bigrams, 3 for trigrams).

    Returns:
        List of n-gram tuples.
    """
    if len(words) < n:
        return []
    return [tuple(words[i : i + n]) for i in range(len(words) - n + 1)]
