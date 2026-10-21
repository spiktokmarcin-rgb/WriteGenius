"""Tests for X (Twitter) and Wykop integration modules."""

from writegenius.integrations.x_client import prepare_x_thread, XClient
from writegenius.integrations.wykop_client import format_wykop_entry, WykopClient


def test_prepare_x_thread_single():
    short_text = "This is a single tweet within the standard limit."
    tweets = prepare_x_thread(short_text, max_chars=280)
    assert len(tweets) == 1
    assert tweets[0] == short_text


def test_prepare_x_thread_multitweet():
    long_text = (
        "WriteGenius delivers accurate readability metrics for European languages. "
        "Standard English metrics fail on Polish and Slavic inflectional morphology. "
        "Our engine implements the official Pisarek Index (1969) with syllable glide detection. "
        "This ensures clean and reliable plain-language assessment for legal and civic documents."
    )
    tweets = prepare_x_thread(long_text, max_chars=120)
    assert len(tweets) > 1
    # Check that pagination suffixes were appended
    assert "(1/" in tweets[0]
    assert f"({len(tweets)}/{len(tweets)})" in tweets[-1]
    # Check length
    for t in tweets:
        assert len(t) <= 120


def test_x_client_dry_run():
    client = XClient(bearer_token=None)
    res = client.post_tweet("Test tweet", dry_run=True)
    assert res["status"] == "dry_run"
    assert "mock_id" in res
    assert res["payload"]["text"] == "Test tweet"

    thread_res = client.post_thread("Sentence one. Sentence two. Sentence three.", dry_run=True)
    assert len(thread_res) >= 1
    assert thread_res[0]["status"] == "dry_run"


def test_format_wykop_entry():
    body = "Nowa wersja WriteGenius jest gotowa na GitHubie."
    tags = ["programowanie", "#python", "opensource"]
    formatted = format_wykop_entry(body, tags=tags)
    assert body in formatted
    assert "#programowanie" in formatted
    assert "#python" in formatted
    assert "#opensource" in formatted
    assert not formatted.endswith("##python")


def test_wykop_client_dry_run():
    client = WykopClient(token=None)
    res = client.create_entry("Nowy wpis", tags=["python"], dry_run=True)
    assert res["status"] == "dry_run"
    assert "payload" in res
    assert "#python" in res["formatted_entry"]


def test_wykop_showcase_draft():
    draft = WykopClient.generate_showcase_draft()
    assert "WriteGenius" in draft
    assert "Pisarka" in draft
    assert "#programowanie" in draft
    assert "github.com/spiktokmarcin-rgb/WriteGenius" in draft
