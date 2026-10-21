"""Rule-based sentiment and subjectivity analyzer for European languages."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Set
from writegenius.core.tokenizers import tokenize_words


@dataclass(frozen=True)
class SentimentResult:
    """Sentiment and subjectivity analysis result."""
    polarity: float       # -1.0 (strongly negative) to +1.0 (strongly positive)
    subjectivity: float   # 0.0 (objective/factual) to 1.0 (highly subjective)
    label: str            # 'positive', 'negative', or 'neutral'

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


# Polish sentiment lexicon
POLISH_POSITIVE: Dict[str, float] = {
    "dobry": 0.6, "świetny": 0.9, "wspaniały": 1.0, "genialny": 1.0,
    "doskonały": 0.9, "rewelacyjny": 0.9, "piękny": 0.7, "pozytywny": 0.6,
    "sukces": 0.8, "zysk": 0.6, "bezpieczny": 0.7, "pomocny": 0.7,
    "skuteczny": 0.8, "atrakcyjny": 0.7, "przyjazny": 0.7, "niezawodny": 0.8,
    "lubić": 0.6, "kochać": 0.9, "polecam": 0.8, "optymalny": 0.7,
    "dobrze": 0.6, "świetnie": 0.9, "wspaniale": 1.0, "skutecznie": 0.8,
}

POLISH_NEGATIVE: Dict[str, float] = {
    "zły": -0.6, "okropny": -0.9, "tragiczny": -1.0, "fatalny": -1.0,
    "błędny": -0.6, "porażka": -0.8, "strata": -0.7, "niebezpieczny": -0.7,
    "wadliwy": -0.7, "awaria": -0.8, "problem": -0.5, "kryzys": -0.8,
    "oszustwo": -0.9, "słaby": -0.6, "beznadziejny": -0.9, "drogi": -0.4,
    "źle": -0.6, "okropnie": -0.9, "fatalnie": -1.0, "słabo": -0.6,
}

POLISH_INTENSIFIERS: Dict[str, float] = {
    "bardzo": 1.5, "niezwykle": 1.7, "wyjątkowo": 1.6, "super": 1.5,
    "mega": 1.5, "ogromnie": 1.6, "naprawdę": 1.3,
    "trochę": 0.6, "nieco": 0.7, "ledwie": 0.5,
}

POLISH_NEGATIONS: Set[str] = {"nie", "brak", "bez", "ani", "nigdy"}


# English sentiment lexicon
ENGLISH_POSITIVE: Dict[str, float] = {
    "good": 0.6, "great": 0.8, "excellent": 0.9, "wonderful": 0.9,
    "brilliant": 1.0, "perfect": 1.0, "beautiful": 0.7, "positive": 0.6,
    "success": 0.8, "secure": 0.7, "helpful": 0.7, "effective": 0.8,
    "reliable": 0.8, "fast": 0.5, "clean": 0.5, "love": 0.9,
    "like": 0.5, "recommended": 0.8, "optimal": 0.7,
}

ENGLISH_NEGATIVE: Dict[str, float] = {
    "bad": -0.6, "terrible": -0.9, "awful": -0.9, "horrible": -1.0,
    "failed": -0.8, "failure": -0.8, "loss": -0.7, "broken": -0.7,
    "buggy": -0.6, "flawed": -0.7, "problem": -0.5, "crisis": -0.8,
    "poor": -0.6, "hopeless": -0.9, "expensive": -0.4, "slow": -0.5,
}

ENGLISH_INTENSIFIERS: Dict[str, float] = {
    "very": 1.5, "extremely": 1.8, "highly": 1.6, "super": 1.5,
    "really": 1.3, "deeply": 1.5,
    "slightly": 0.6, "barely": 0.5, "somewhat": 0.7,
}

ENGLISH_NEGATIONS: Set[str] = {"not", "no", "never", "without", "hardly", "barely"}


def analyze_sentiment(text: str, lang: str = "pl") -> SentimentResult:
    """Analyze sentiment polarity and subjectivity.

    Handles language-specific lexicons, negation flipping, and modifier intensifiers.

    Args:
        text: Input text string.
        lang: Target language ('pl' or 'en', defaults to 'pl').

    Returns:
        SentimentResult containing polarity (-1..1), subjectivity (0..1), and classification.
    """
    if not text or not text.strip():
        return SentimentResult(polarity=0.0, subjectivity=0.0, label="neutral")

    words = [w.lower() for w in tokenize_words(text)]
    if not words:
        return SentimentResult(polarity=0.0, subjectivity=0.0, label="neutral")

    # Select language dictionaries
    if lang == "pl":
        pos_dict = POLISH_POSITIVE
        neg_dict = POLISH_NEGATIVE
        intensifiers = POLISH_INTENSIFIERS
        negations = POLISH_NEGATIONS
    else:
        pos_dict = ENGLISH_POSITIVE
        neg_dict = ENGLISH_NEGATIVE
        intensifiers = ENGLISH_INTENSIFIERS
        negations = ENGLISH_NEGATIONS

    total_polarity = 0.0
    sentiment_word_count = 0
    negation_window = 0
    current_modifier = 1.0

    for word in words:
        # Check if current token is a negation
        if word in negations:
            negation_window = 3  # Affects next 2-3 words
            continue

        # Check if current token is an intensifier
        if word in intensifiers:
            current_modifier = intensifiers[word]
            continue

        # Look for match in polarity lexicon
        word_score = None
        if word in pos_dict:
            word_score = pos_dict[word]
        elif word in neg_dict:
            word_score = neg_dict[word]

        if word_score is not None:
            # Apply negation flip if active
            if negation_window > 0:
                word_score = -word_score * 0.8
                negation_window = 0

            # Apply modifier
            word_score *= current_modifier
            current_modifier = 1.0

            total_polarity += word_score
            sentiment_word_count += 1
        else:
            if negation_window > 0:
                negation_window -= 1

    if sentiment_word_count == 0:
        return SentimentResult(polarity=0.0, subjectivity=0.0, label="neutral")

    # Normalize polarity between -1.0 and 1.0
    norm_polarity = max(-1.0, min(1.0, total_polarity / sentiment_word_count))
    # Subjectivity reflects the concentration of emotive/polar words
    subjectivity = min(1.0, round(sentiment_word_count / len(words) * 3.5, 2))

    if norm_polarity > 0.15:
        label = "positive"
    elif norm_polarity < -0.15:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResult(
        polarity=round(norm_polarity, 3),
        subjectivity=subjectivity,
        label=label,
    )
