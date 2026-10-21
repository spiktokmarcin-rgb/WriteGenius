"""Tests for the unified pipeline."""

from writegenius.pipeline import analyze_text


def test_analyze_text_polish():
    text = (
        "WriteGenius to nowoczesna biblioteka przetwarzania języka naturalnego. "
        "Umożliwia szybką analizę czytelności i bogactwa słownictwa dla języków europejskich."
    )
    report = analyze_text(text)
    assert report.language == "pl"
    assert report.statistics.word_count > 10
    assert report.polish_metrics is not None
    assert report.polish_metrics.pisarek_index > 0
    assert report.lexical_diversity.type_token_ratio > 0

    json_str = report.to_json()
    assert "pisarek_index" in json_str

    summary_str = report.summary()
    assert "WriteGenius Text Analysis Report" in summary_str


def test_analyze_text_english():
    text = "WriteGenius delivers fast linguistic evaluation for European languages."
    report = analyze_text(text, lang="en")
    assert report.language == "en"
    assert report.readability.flesch_reading_ease != 0
