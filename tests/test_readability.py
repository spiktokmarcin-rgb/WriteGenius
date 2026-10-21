"""Tests for general European readability calculations."""

from writegenius.metrics.readability import compute_readability_suite


def test_compute_readability_english():
    text = (
        "The quick brown fox jumps over the lazy dog. "
        "This is an elementary reading passage designed for clear understanding."
    )
    scores = compute_readability_suite(text, lang="en")
    assert scores.flesch_reading_ease > 50.0
    assert scores.flesch_kincaid_grade > 0.0
    assert scores.gunning_fog > 0.0


def test_empty_readability():
    scores = compute_readability_suite("", lang="en")
    assert scores.flesch_reading_ease == 0.0
    assert scores.gunning_fog == 0.0
