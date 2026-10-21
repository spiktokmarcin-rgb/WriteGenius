"""NLP processing, stopwords, normalization, and sentiment analysis."""

from writegenius.nlp.stopwords import get_stopwords, remove_stopwords
from writegenius.nlp.normalizer import (
    strip_diacritics,
    normalize_whitespace,
    clean_text,
    detect_language_heuristic,
)
from writegenius.nlp.sentiment import analyze_sentiment, SentimentResult

__all__ = [
    "get_stopwords",
    "remove_stopwords",
    "strip_diacritics",
    "normalize_whitespace",
    "clean_text",
    "detect_language_heuristic",
    "analyze_sentiment",
    "SentimentResult",
]
