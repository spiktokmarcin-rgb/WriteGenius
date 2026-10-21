"""Tests for Reddit and X social media linguistic analytics."""

from writegenius.integrations.social_analyzer import (
    SocialPost,
    analyze_social_posts,
    parse_x_timeline,
)


def test_social_post_dataclass():
    post = SocialPost(id="123", platform="reddit", text="Przykładowy wpis o programowaniu.", author="tester")
    d = post.to_dict()
    assert d["id"] == "123"
    assert d["platform"] == "reddit"
    assert "programowaniu" in d["text"]


def test_analyze_social_posts_polish():
    posts = [
        SocialPost(id="1", platform="reddit", text="Świetny nowy projekt open source dla programistów w Polsce! Bardzo polecam."),
        SocialPost(id="2", platform="reddit", text="Nowe zasady podatkowe dla programistów i przedsiębiorców wchodzą od nowego kwartału."),
        SocialPost(id="3", platform="reddit", text="Niestety wystąpił okropny błąd w bibliotece i system zanotował awarię."),
    ]
    report = analyze_social_posts(posts, lang="pl")

    assert report.platform == "reddit"
    assert report.total_posts == 3
    assert report.total_words > 15
    assert report.dominant_language == "pl"
    assert report.readability_metric_name == "Avg Indeks Pisarka (W)"
    assert report.avg_readability_score > 0
    # Sentiment distribution must have positive, neutral, and negative entries
    assert "positive" in report.sentiment_distribution
    assert "negative" in report.sentiment_distribution
    assert report.sentiment_distribution["positive"] > 0
    assert report.sentiment_distribution["negative"] > 0

    summary = report.summary()
    assert "WriteGenius Social Media Linguistic Audit" in summary


def test_analyze_social_posts_english():
    posts = [
        SocialPost(id="x1", platform="x", text="This is an extraordinary and clean Python library for linguistic evaluation."),
        SocialPost(id="x2", platform="x", text="Standard formulas fail on complex languages due to inflectional suffixes."),
    ]
    report = analyze_social_posts(posts, lang="en")
    assert report.platform == "x"
    assert report.dominant_language == "en"
    assert report.readability_metric_name == "Avg Flesch Reading Ease"
    assert report.type_token_ratio > 0.5


def test_parse_x_timeline():
    raw_tweets = [
        {
            "id": "18000000001",
            "text": "Announcing WriteGenius 0.1.0: Multilingual NLP for European languages.",
            "author_id": "9999",
            "public_metrics": {"like_count": 42},
            "created_at": "2026-10-21T12:00:00Z",
        },
        {
            "id": "18000000002",
            "text": "Read the empirical benchmark vs textstat and spaCy.",
            "author_id": "9999",
            "public_metrics": {"like_count": 15},
            "created_at": "2026-10-21T12:05:00Z",
        },
    ]
    posts = parse_x_timeline(raw_tweets)
    assert len(posts) == 2
    assert posts[0].id == "18000000001"
    assert posts[0].platform == "x"
    assert posts[0].score == 42
    assert "WriteGenius" in posts[0].text


def test_empty_social_posts():
    report = analyze_social_posts([])
    assert report.total_posts == 0
    assert report.total_words == 0
