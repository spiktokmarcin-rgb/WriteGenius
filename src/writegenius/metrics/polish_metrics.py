"""Readability formulas specifically calibrated for the Polish language."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
from writegenius.core.tokenizers import tokenize_words, tokenize_sentences, count_syllables_polish


@dataclass(frozen=True)
class PolishReadabilityResult:
    """Result of Polish readability evaluations."""
    pisarek_index: float
    pisarek_difficulty_level: str
    pisarek_target_audience: str
    fog_polish: float
    hard_words_ratio_percent: float
    avg_sentence_length: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_pisarek_index(text: str) -> PolishReadabilityResult:
    """Calculate the Pisarek Readability Index (Walery Pisarek, 1969).

    In Polish linguistics, Pisarek's formula is the premier empirical readability metric.
    Unlike English formulas that treat 3-syllable words as complex, Polish inflection
    naturally extends word lengths, meaning words with 4 or more syllables
    represent genuine cognitive complexity.

    Formula:
        W = (T / Z) + (B / T) * 100

        where:
        T = Total word count
        Z = Total sentence count
        B = Count of 'hard words' (syllables >= 4)

    Interpretation scale:
        < 18: Very easy (prosty, dla każdego)
        18 - 25: Easy (prasa codzienna, komunikacja masowa)
        26 - 33: Average (wymaga szkoły średniej)
        34 - 41: Difficult (teksty specjalistyczne, akademickie)
        >= 42: Very difficult (żargon prawniczy, urzędowy)

    Args:
        text: Input Polish text string.

    Returns:
        PolishReadabilityResult dataclass.
    """
    if not text or not text.strip():
        return PolishReadabilityResult(
            pisarek_index=0.0,
            pisarek_difficulty_level="Brak danych",
            pisarek_target_audience="N/A",
            fog_polish=0.0,
            hard_words_ratio_percent=0.0,
            avg_sentence_length=0.0,
        )

    sentences = tokenize_sentences(text)
    words = tokenize_words(text)

    num_words = len(words)
    num_sentences = max(1, len(sentences))

    if num_words == 0:
        return PolishReadabilityResult(
            pisarek_index=0.0,
            pisarek_difficulty_level="Brak danych",
            pisarek_target_audience="N/A",
            fog_polish=0.0,
            hard_words_ratio_percent=0.0,
            avg_sentence_length=0.0,
        )

    # Count Polish hard words (syllables >= 4)
    hard_words = sum(1 for w in words if count_syllables_polish(w) >= 4)

    # Average sentence length: words per sentence
    avg_sent_len = num_words / num_sentences

    # Percentage of hard words (0..100)
    hard_ratio = (hard_words / num_words) * 100.0

    # Pisarek formula
    w_score = avg_sent_len + hard_ratio

    # Polish FOG adaptation (0.4 * (avg_sent_len + hard_ratio))
    fog_pl = 0.4 * (avg_sent_len + hard_ratio)

    if w_score < 18.0:
        level = "Bardzo łatwy (klasy 1-6)"
        audience = "Szeroka publiczność, dzieci, proste instrukcje"
    elif w_score < 26.0:
        level = "Łatwy (szkoła podstawowa / prasa masowa)"
        audience = "Prasa codzienna, portale informacyjne, blogi"
    elif w_score < 34.0:
        level = "Przeciętny (szkoła średnia)"
        audience = "Czasopisma branżowe, literatura popularnonaukowa"
    elif w_score < 42.0:
        level = "Trudny (wykształcenie wyższe)"
        audience = "Artykuły naukowe, podręczniki akademickie, prawo gospodarcze"
    else:
        level = "Bardzo trudny (język urzędowy/akademicki)"
        audience = "Specjaliści, prawnicy, publikacje habilitacyjne"

    return PolishReadabilityResult(
        pisarek_index=round(w_score, 2),
        pisarek_difficulty_level=level,
        pisarek_target_audience=audience,
        fog_polish=round(fog_pl, 2),
        hard_words_ratio_percent=round(hard_ratio, 2),
        avg_sentence_length=round(avg_sent_len, 2),
    )
