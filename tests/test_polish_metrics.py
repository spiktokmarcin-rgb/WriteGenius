"""Tests for Polish-specific readability metrics."""

import pytest
from writegenius.metrics.polish_metrics import calculate_pisarek_index


def test_pisarek_simple_text():
    # Simple sentences with short words
    text = "Mama ma psa. Tata ma kota. Kot pije mleko. Pies biega po łące."
    result = calculate_pisarek_index(text)
    assert result.pisarek_index < 20.0
    assert "łatwy" in result.pisarek_difficulty_level.lower()
    assert result.hard_words_ratio_percent == 0.0


def test_pisarek_complex_text():
    # Text with long, polysyllabic administrative/scientific words
    text = (
        "Zaimplementowana funkcjonalność umożliwia wieloaspektową parametryzację "
        "algorytmów sztucznej inteligencji w środowiskach teleinformatycznych."
    )
    result = calculate_pisarek_index(text)
    # Average sentence is 12 words, but heavy on 4+ syllable words
    assert result.hard_words_ratio_percent > 30.0
    assert result.pisarek_index > 25.0
