"""Core text processing and statistics modules."""

from writegenius.core.tokenizers import (
    tokenize_words,
    tokenize_sentences,
    count_syllables,
    count_syllables_polish,
    extract_ngrams,
)
from writegenius.core.text_stats import TextStatistics, compute_text_stats

__all__ = [
    "tokenize_words",
    "tokenize_sentences",
    "count_syllables",
    "count_syllables_polish",
    "extract_ngrams",
    "TextStatistics",
    "compute_text_stats",
]
