"""X (Twitter) API v2 integration and thread segmentation for WriteGenius."""

from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
from writegenius.core.tokenizers import tokenize_sentences


def prepare_x_thread(text: str, max_chars: int = 280) -> List[str]:
    """Segment an article or report into cohesive X (Twitter) thread posts.

    Respects sentence boundaries and appends index indicators (e.g. '1/4', '2/4')
    only when text requires more than one post.

    Args:
        text: Input string.
        max_chars: Maximum characters per tweet (standard is 280).

    Returns:
        List of formatted tweet strings.
    """
    if not text or not text.strip():
        return []

    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return [cleaned]

    sentences = tokenize_sentences(cleaned)
    if not sentences:
        return [cleaned[:max_chars]]

    # Reserve room for pagination suffix, e.g. " (1/10)"
    suffix_buffer = 10
    limit = max_chars - suffix_buffer

    chunks: List[str] = []
    current_chunk: List[str] = []
    current_len = 0

    for sent in sentences:
        sent_len = len(sent)
        if current_len + sent_len + 1 <= limit:
            current_chunk.append(sent)
            current_len += sent_len + 1
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            # If a single sentence exceeds the limit, hard-slice it
            if sent_len > limit:
                words = sent.split()
                sub_chunk: List[str] = []
                sub_len = 0
                for w in words:
                    if sub_len + len(w) + 1 <= limit:
                        sub_chunk.append(w)
                        sub_len += len(w) + 1
                    else:
                        if sub_chunk:
                            chunks.append(" ".join(sub_chunk))
                        sub_chunk = [w]
                        sub_len = len(w)
                if sub_chunk:
                    current_chunk = sub_chunk
                    current_len = sub_len
                else:
                    current_chunk = []
                    current_len = 0
            else:
                current_chunk = [sent]
                current_len = sent_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    total = len(chunks)
    if total <= 1:
        return chunks

    return [f"{chunk} ({i + 1}/{total})" for i, chunk in enumerate(chunks)]


class XClient:
    """Lightweight client for X (Twitter) API v2 endpoints."""

    def __init__(self, bearer_token: Optional[str] = None):
        self.bearer_token = bearer_token or os.getenv("X_BEARER_TOKEN") or os.getenv("TWITTER_BEARER_TOKEN")
        self.api_url = "https://api.twitter.com/2/tweets"

    def post_tweet(self, text: str, in_reply_to_tweet_id: Optional[str] = None, dry_run: bool = False) -> Dict[str, Any]:
        """Post a single tweet via X API v2.

        Args:
            text: Text content (max 280 chars).
            in_reply_to_tweet_id: Optional ID to reply to.
            dry_run: If True, validates payload without making network calls.

        Returns:
            Dictionary with response or dry-run payload.
        """
        payload: Dict[str, Any] = {"text": text}
        if in_reply_to_tweet_id:
            payload["reply"] = {"in_reply_to_tweet_id": in_reply_to_tweet_id}

        if dry_run or not self.bearer_token:
            return {
                "status": "dry_run",
                "mock_id": f"mock_tweet_{abs(hash(text)) % 1000000}",
                "payload": payload,
                "token_present": bool(self.bearer_token),
            }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "User-Agent": "WriteGenius-Publisher/0.1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            return {"error": e.code, "message": error_body}

    def post_thread(self, text_or_tweets: str | List[str], dry_run: bool = False) -> List[Dict[str, Any]]:
        """Publish a sequence of chained tweets as an X thread.

        Args:
            text_or_tweets: Long text string or pre-split list of tweets.
            dry_run: If True, simulates posting without network calls.

        Returns:
            List of responses per tweet in the thread.
        """
        if isinstance(text_or_tweets, str):
            tweets = prepare_x_thread(text_or_tweets)
        else:
            tweets = text_or_tweets

        responses: List[Dict[str, Any]] = []
        last_id: Optional[str] = None

        for tweet in tweets:
            res = self.post_tweet(tweet, in_reply_to_tweet_id=last_id, dry_run=dry_run)
            responses.append(res)
            # Extract id for chaining
            last_id = res.get("data", {}).get("id") or res.get("mock_id")

        return responses
