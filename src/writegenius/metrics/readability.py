"""General European and international readability formulas."""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
from writegenius.core.tokenizers import tokenize_words, tokenize_sentences, count_syllables


@dataclass(frozen=True)
class ReadabilityScores:
    """Consolidated readability test results."""
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog: float
    automated_readability_index: float
    coleman_liau_index: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_flesch_reading_ease(
    words_count: int,
    sentences_count: int,
    syllables_count: int,
    lang: str = "en",
) -> float:
    """Calculate Flesch Reading Ease score.

    Score ranges:
        90-100: Very Easy (5th grade)
        80-89: Easy (6th grade)
        70-79: Fairly Easy (7th grade)
        60-69: Standard (8th-9th grade)
        50-59: Fairly Difficult (10th-12th grade)
        30-49: Difficult (College)
        0-29: Very Confusing (Graduate)
    """
    if words_count == 0 or sentences_count == 0:
        return 0.0

    asl = words_count / sentences_count
    asw = syllables_count / words_count

    if lang == "de":
        # Amstad adaptation for German
        score = 180.0 - asl - (58.5 * asw)
    elif lang == "fr":
        # Kandel & Moles adaptation for French
        score = 207.0 - (1.015 * asl) - (73.6 * asw)
    elif lang == "es":
        # Fernandez-Huerta adaptation for Spanish
        score = 206.84 - (1.02 * asl) - (60.0 * asw)
    else:
        # Standard English formula
        score = 206.835 - (1.015 * asl) - (84.6 * asw)

    return round(score, 2)


def calculate_flesch_kincaid_grade(
    words_count: int,
    sentences_count: int,
    syllables_count: int,
) -> float:
    """Calculate Flesch-Kincaid Grade Level."""
    if words_count == 0 or sentences_count == 0:
        return 0.0

    asl = words_count / sentences_count
    asw = syllables_count / words_count
    grade = (0.39 * asl) + (11.8 * asw) - 15.59
    return max(0.0, round(grade, 2))


def calculate_gunning_fog(
    words_count: int,
    sentences_count: int,
    complex_words_count: int,
) -> float:
    """Calculate Gunning Fog Index."""
    if words_count == 0 or sentences_count == 0:
        return 0.0

    asl = words_count / sentences_count
    hard_percent = (complex_words_count / words_count) * 100.0
    fog = 0.4 * (asl + hard_percent)
    return round(fog, 2)


def calculate_coleman_liau(
    letters_count: int,
    words_count: int,
    sentences_count: int,
) -> float:
    """Calculate Coleman-Liau Index."""
    if words_count == 0:
        return 0.0

    l_score = (letters_count / words_count) * 100.0
    s_score = (sentences_count / words_count) * 100.0
    cli = (0.0588 * l_score) - (0.296 * s_score) - 15.8
    return round(cli, 2)


def calculate_ari(
    characters_no_spaces: int,
    words_count: int,
    sentences_count: int,
) -> float:
    """Calculate Automated Readability Index (ARI)."""
    if words_count == 0 or sentences_count == 0:
        return 0.0

    ari = 4.71 * (characters_no_spaces / words_count) + 0.5 * (words_count / sentences_count) - 21.43
    return round(ari, 2)


def compute_readability_suite(text: str, lang: str = "en") -> ReadabilityScores:
    """Compute all standard readability scores in one pass."""
    if not text or not text.strip():
        return ReadabilityScores(0.0, 0.0, 0.0, 0.0, 0.0)

    words = tokenize_words(text)
    sentences = tokenize_sentences(text)

    num_words = len(words)
    num_sentences = max(1, len(sentences))
    if num_words == 0:
        return ReadabilityScores(0.0, 0.0, 0.0, 0.0, 0.0)

    syllables = [count_syllables(w, lang=lang) for w in words]
    total_syllables = sum(syllables)
    complex_words = sum(1 for s in syllables if s >= 3)
    total_letters = sum(len(w) for w in words)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))

    fre = calculate_flesch_reading_ease(num_words, num_sentences, total_syllables, lang=lang)
    fkg = calculate_flesch_kincaid_grade(num_words, num_sentences, total_syllables)
    fog = calculate_gunning_fog(num_words, num_sentences, complex_words)
    cli = calculate_coleman_liau(total_letters, num_words, num_sentences)
    ari = calculate_ari(chars_no_spaces, num_words, num_sentences)

    return ReadabilityScores(
        flesch_reading_ease=fre,
        flesch_kincaid_grade=fkg,
        gunning_fog=fog,
        automated_readability_index=ari,
        coleman_liau_index=cli,
    )
