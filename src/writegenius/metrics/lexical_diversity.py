"""Lexical richness, diversity, and vocabulary statistics."""

from __future__ import annotations
import math
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from writegenius.nlp.stopwords import get_stopwords


@dataclass(frozen=True)
class LexicalDiversityResult:
    """Measures of vocabulary richness and lexical variety."""
    type_token_ratio: float       # TTR = Types / Tokens (0..1)
    root_ttr: float               # Guiraud's index = Types / sqrt(Tokens)
    hapax_legomena_count: int     # Words occurring exactly once
    hapax_ratio: float            # Hapax / Total Tokens
    lexical_density: float        # Content words (non-stopwords) / Total Tokens

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_lexical_diversity(words: List[str], lang: str = "pl") -> LexicalDiversityResult:
    """Calculate comprehensive lexical richness metrics.

    Args:
        words: List of tokenized words.
        lang: Language code for stopword resolution.

    Returns:
        LexicalDiversityResult dataclass.
    """
    total_tokens = len(words)
    if total_tokens == 0:
        return LexicalDiversityResult(
            type_token_ratio=0.0,
            root_ttr=0.0,
            hapax_legomena_count=0,
            hapax_ratio=0.0,
            lexical_density=0.0,
        )

    # Lowercase tokens for lexical analysis
    lowered = [w.lower() for w in words]
    counts = Counter(lowered)
    unique_types = len(counts)

    ttr = round(unique_types / total_tokens, 3)
    root_ttr = round(unique_types / math.sqrt(total_tokens), 3)

    hapax_count = sum(1 for count in counts.values() if count == 1)
    hapax_ratio = round(hapax_count / total_tokens, 3)

    stops = get_stopwords(lang)
    content_words = [w for w in lowered if w not in stops]
    density = round(len(content_words) / total_tokens, 3)

    return LexicalDiversityResult(
        type_token_ratio=ttr,
        root_ttr=root_ttr,
        hapax_legomena_count=hapax_count,
        hapax_ratio=hapax_ratio,
        lexical_density=density,
    )
