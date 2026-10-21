"""WriteGenius: Multilingual Natural Language Processing & Readability Engine for European Languages.

WriteGenius provides specialized linguistic tools, readability metrics, and text quality scoring
calibrated specifically for European languages, with first-class support for Polish, English,
German, French, Spanish, and more.
"""

__version__ = "0.1.0"
__author__ = "WriteGenius Contributors"
__license__ = "MIT"

from writegenius.pipeline import analyze_text, TextAnalysisReport
from writegenius.core.tokenizers import (
    tokenize_words,
    tokenize_sentences,
    count_syllables,
    count_syllables_polish,
    extract_ngrams,
)
from writegenius.core.text_stats import compute_text_stats, TextStatistics
from writegenius.nlp.normalizer import (
    strip_diacritics,
    clean_text,
    detect_language_heuristic,
)
from writegenius.nlp.stopwords import get_stopwords, remove_stopwords
from writegenius.nlp.sentiment import analyze_sentiment, SentimentResult
from writegenius.metrics.polish_metrics import (
    calculate_pisarek_index,
    PolishReadabilityResult,
)
from writegenius.metrics.readability import (
    compute_readability_suite,
    calculate_flesch_reading_ease,
    calculate_flesch_kincaid_grade,
    calculate_gunning_fog,
    ReadabilityScores,
)
from writegenius.metrics.lexical_diversity import (
    calculate_lexical_diversity,
    LexicalDiversityResult,
)
from writegenius.integrations import (
    XClient,
    prepare_x_thread,
    WykopClient,
    format_wykop_entry,
)

__all__ = [
    "__version__",
    "analyze_text",
    "TextAnalysisReport",
    "tokenize_words",
    "tokenize_sentences",
    "count_syllables",
    "count_syllables_polish",
    "extract_ngrams",
    "compute_text_stats",
    "TextStatistics",
    "strip_diacritics",
    "clean_text",
    "detect_language_heuristic",
    "get_stopwords",
    "remove_stopwords",
    "analyze_sentiment",
    "SentimentResult",
    "calculate_pisarek_index",
    "PolishReadabilityResult",
    "compute_readability_suite",
    "calculate_flesch_reading_ease",
    "calculate_flesch_kincaid_grade",
    "calculate_gunning_fog",
    "ReadabilityScores",
    "calculate_lexical_diversity",
    "LexicalDiversityResult",
    "XClient",
    "prepare_x_thread",
    "WykopClient",
    "format_wykop_entry",
]
