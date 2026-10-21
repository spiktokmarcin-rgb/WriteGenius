"""Benchmark tests against the reference multilingual corpus."""

import json
from pathlib import Path
from writegenius.pipeline import analyze_text
from writegenius.metrics.polish_metrics import calculate_pisarek_index

CORPUS_PATH = Path(__file__).resolve().parent.parent / "data" / "benchmark_corpus.json"


def test_polish_benchmark_evaluation():
    assert CORPUS_PATH.exists(), "Benchmark corpus file missing"
    data = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))

    pl_samples = {s["id"]: s for s in data["samples"] if s["language"] == "pl"}
    assert len(pl_samples) >= 4

    tier1 = calculate_pisarek_index(pl_samples["pl_tier1_01"]["text"])
    tier4 = calculate_pisarek_index(pl_samples["pl_tier4_01"]["text"])

    # Elementary text must have a much lower cognitive difficulty score than statutory legal text
    assert tier1.pisarek_index < 18.0
    assert "łatwy" in tier1.pisarek_difficulty_level.lower()
    assert tier4.pisarek_index > 34.0
    assert "trudny" in tier4.pisarek_difficulty_level.lower()
    assert tier4.pisarek_index > tier1.pisarek_index * 2


def test_english_benchmark_evaluation():
    data = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    en_samples = {s["id"]: s for s in data["samples"] if s["language"] == "en"}
    assert len(en_samples) >= 3

    tier1 = analyze_text(en_samples["en_tier1_01"]["text"], lang="en")
    tier4 = analyze_text(en_samples["en_tier4_01"]["text"], lang="en")

    # Tier 1 (elementary) should have a high reading ease, Tier 4 (technical whitepaper) should be very low
    assert tier1.readability.flesch_reading_ease > 80.0
    assert tier4.readability.flesch_reading_ease < 30.0
