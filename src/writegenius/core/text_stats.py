"""Core statistical metrics for written texts."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from writegenius.core.tokenizers import (
    tokenize_words,
    tokenize_sentences,
    count_syllables,
)


@dataclass(frozen=True)
class TextStatistics:
    """Summary of basic surface-level text statistics."""
    character_count: int
    character_count_no_spaces: int
    word_count: int
    sentence_count: int
    syllable_count: int
    avg_word_length: float
    avg_sentence_length: float
    avg_syllables_per_word: float
    polysyllabic_words: int  # Words with >= 3 syllables (FOG standard)
    hard_words_polish: int    # Words with >= 4 syllables (Pisarek standard)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def compute_text_stats(text: str, lang: str = "pl") -> TextStatistics:
    """Compute comprehensive surface statistics for a text.

    Args:
        text: Input string.
        lang: Target language code ('pl', 'en', etc.).

    Returns:
        TextStatistics dataclass.
    """
    if not text or not text.strip():
        return TextStatistics(
            character_count=0,
            character_count_no_spaces=0,
            word_count=0,
            sentence_count=0,
            syllable_count=0,
            avg_word_length=0.0,
            avg_sentence_length=0.0,
            avg_syllables_per_word=0.0,
            polysyllabic_words=0,
            hard_words_polish=0,
        )

    sentences = tokenize_sentences(text)
    words = tokenize_words(text)

    char_count = len(text)
    char_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", ""))
    word_count = len(words)
    sentence_count = max(1, len(sentences))

    if word_count == 0:
        return TextStatistics(
            character_count=char_count,
            character_count_no_spaces=char_no_spaces,
            word_count=0,
            sentence_count=sentence_count,
            syllable_count=0,
            avg_word_length=0.0,
            avg_sentence_length=0.0,
            avg_syllables_per_word=0.0,
            polysyllabic_words=0,
            hard_words_polish=0,
        )

    syllable_counts = [count_syllables(w, lang=lang) for w in words]
    total_syllables = sum(syllable_counts)

    polysyllabic_3 = sum(1 for s in syllable_counts if s >= 3)
    hard_words_4 = sum(1 for s in syllable_counts if s >= 4)

    total_chars_in_words = sum(len(w) for w in words)
    avg_word_len = round(total_chars_in_words / word_count, 2)
    avg_sent_len = round(word_count / sentence_count, 2)
    avg_syllables = round(total_syllables / word_count, 2)

    return TextStatistics(
        character_count=char_count,
        character_count_no_spaces=char_no_spaces,
        word_count=word_count,
        sentence_count=sentence_count,
        syllable_count=total_syllables,
        avg_word_length=avg_word_len,
        avg_sentence_length=avg_sent_len,
        avg_syllables_per_word=avg_syllables,
        polysyllabic_words=polysyllabic_3,
        hard_words_polish=hard_words_4,
    )
