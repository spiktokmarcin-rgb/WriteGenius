"""Tests for sentiment and subjectivity analysis."""

from writegenius.nlp.sentiment import analyze_sentiment


def test_positive_sentiment_polish():
    text = "Ten nowy system jest wspaniały, genialny i bardzo skuteczny."
    res = analyze_sentiment(text, lang="pl")
    assert res.polarity > 0.4
    assert res.label == "positive"
    assert res.subjectivity > 0.0


def test_negative_sentiment_polish():
    text = "To była fatalna porażka i okropny problem."
    res = analyze_sentiment(text, lang="pl")
    assert res.polarity < -0.4
    assert res.label == "negative"


def test_negation_flip():
    positive_text = "Ten algorytm jest dobry."
    negated_text = "Ten algorytm nie jest dobry."

    pos_res = analyze_sentiment(positive_text, lang="pl")
    neg_res = analyze_sentiment(negated_text, lang="pl")

    assert pos_res.polarity > 0.0
    assert neg_res.polarity < 0.0


def test_sentiment_english():
    text = "This repository offers an excellent and clean implementation."
    res = analyze_sentiment(text, lang="en")
    assert res.polarity > 0.3
    assert res.label == "positive"
