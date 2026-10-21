"""Tests for tokenization and syllable counting."""

import pytest
from writegenius.core.tokenizers import (
    tokenize_words,
    tokenize_sentences,
    count_syllables_polish,
    count_syllables,
    extract_ngrams,
)


def test_tokenize_sentences_abbreviations():
    text = "Prof. Jan Kowalski mieszka przy ul. Polnej w Warszawie. To jest m.in. ciekawe, np. dla studentów."
    sentences = tokenize_sentences(text)
    assert len(sentences) == 2
    assert "Prof. Jan Kowalski" in sentences[0]
    assert "studentów." in sentences[1]


def test_tokenize_words():
    text = "Zażółć, gęślą jaźń! WriteGenius wspiera język polski."
    words = tokenize_words(text)
    assert "Zażółć" in words
    assert "gęślą" in words
    assert "WriteGenius" in words
    assert "!" not in words
    assert "," not in words


def test_count_syllables_polish_diphthongs():
    # 'nie-bo' -> 2 syllables (ie is a glide, not two separate vowels)
    assert count_syllables_polish("niebo") == 2
    # 'zro-bić' -> 2 syllables
    assert count_syllables_polish("zrobić") == 2
    # 'zro-bię' -> 2 syllables
    assert count_syllables_polish("zrobię") == 2
    # 'ma-te-ma-ty-ka' -> 5 syllables
    assert count_syllables_polish("matematyka") == 5
    # Single syllable
    assert count_syllables_polish("pies") == 1
    assert count_syllables_polish("kot") == 1


def test_extract_ngrams():
    tokens = ["szybki", "brązowy", "lis", "skacze"]
    bigrams = extract_ngrams(tokens, n=2)
    assert len(bigrams) == 3
    assert bigrams[0] == ("szybki", "brązowy")
    assert bigrams[2] == ("lis", "skacze")
