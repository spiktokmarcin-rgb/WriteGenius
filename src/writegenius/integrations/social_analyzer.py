"""Social media analytics engine for Reddit and X.com (Twitter)."""

from __future__ import annotations
import json
import urllib.request
import urllib.error
from collections import Counter
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

from writegenius.core.tokenizers import tokenize_words
from writegenius.nlp.stopwords import remove_stopwords
from writegenius.nlp.sentiment import analyze_sentiment
from writegenius.nlp.normalizer import detect_language_heuristic
from writegenius.metrics.polish_metrics import calculate_pisarek_index
from writegenius.metrics.readability import compute_readability_suite


@dataclass
class SocialPost:
    """Standardized representation of a social media post or comment."""
    id: str
    platform: str         # 'reddit' or 'x'
    text: str
    author: Optional[str] = None
    score: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SocialBatchReport:
    """Aggregated linguistic, sentiment, and readability metrics for a social feed."""
    platform: str
    total_posts: int
    total_words: int
    dominant_language: str
    avg_sentence_length: float
    sentiment_distribution: Dict[str, float]  # {'positive': %, 'neutral': %, 'negative': %}
    avg_polarity: float
    avg_readability_score: float             # Pisarek for PL, Flesch for others
    readability_metric_name: str
    type_token_ratio: float                   # Global TTR across the feed
    top_keywords: List[Dict[str, Any]]        # Top non-stopword terms

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def summary(self) -> str:
        lines = [
            "=" * 60,
            f" WriteGenius Social Media Linguistic Audit: {self.platform.upper()}",
            "=" * 60,
            f"Analyzed Posts: {self.total_posts} | Total Words: {self.total_words} | Lang: {self.dominant_language.upper()}",
            f"Sentiment: Positive {self.sentiment_distribution['positive']}% | Neutral {self.sentiment_distribution['neutral']}% | Negative {self.sentiment_distribution['negative']}%",
            f"Average Polarity: {self.avg_polarity} (-1.0 to +1.0)",
            f"{self.readability_metric_name}: {self.avg_readability_score}",
            f"Collective Type-Token Ratio (TTR): {self.type_token_ratio}",
            "-" * 60,
            "Top Content Keywords:",
        ]
        for kw in self.top_keywords[:8]:
            lines.append(f" • {kw['word']}: {kw['count']} occurrences")
        lines.append("=" * 60)
        return "\n".join(lines)


def analyze_social_posts(posts: List[SocialPost], lang: Optional[str] = None) -> SocialBatchReport:
    """Analyze a collection of Reddit or X posts for readability, sentiment, and keyword density.

    Args:
        posts: List of SocialPost objects.
        lang: Target language. If None, detected from corpus.

    Returns:
        SocialBatchReport with aggregated statistics.
    """
    if not posts:
        return SocialBatchReport(
            platform="unknown",
            total_posts=0,
            total_words=0,
            dominant_language=lang or "en",
            avg_sentence_length=0.0,
            sentiment_distribution={"positive": 0.0, "neutral": 0.0, "negative": 0.0},
            avg_polarity=0.0,
            avg_readability_score=0.0,
            readability_metric_name="N/A",
            type_token_ratio=0.0,
            top_keywords=[],
        )

    platform = posts[0].platform if posts else "social"
    combined_text = " ".join(p.text for p in posts)
    detected_lang = lang or detect_language_heuristic(combined_text)

    all_words: List[str] = []
    polarities: List[float] = []
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    readability_scores: List[float] = []

    for post in posts:
        text = post.text.strip()
        if not text:
            continue

        words = tokenize_words(text)
        all_words.extend([w.lower() for w in words])

        # Sentiment evaluation
        sent = analyze_sentiment(text, lang=detected_lang)
        polarities.append(sent.polarity)
        sentiment_counts[sent.label] += 1

        # Readability evaluation
        if detected_lang == "pl":
            p_res = calculate_pisarek_index(text)
            readability_scores.append(p_res.pisarek_index)
        else:
            r_res = compute_readability_suite(text, lang=detected_lang)
            readability_scores.append(r_res.flesch_reading_ease)

    total_evaluated = max(1, len(posts))
    total_words = len(all_words)

    # Sentiment percentages
    sent_dist = {
        k: round((v / total_evaluated) * 100.0, 1) for k, v in sentiment_counts.items()
    }
    avg_pol = round(sum(polarities) / len(polarities), 3) if polarities else 0.0

    # Readability average
    avg_read = round(sum(readability_scores) / len(readability_scores), 2) if readability_scores else 0.0
    metric_name = "Avg Indeks Pisarka (W)" if detected_lang == "pl" else "Avg Flesch Reading Ease"

    # Lexical richness
    unique_words = len(set(all_words))
    ttr = round(unique_words / total_words, 3) if total_words > 0 else 0.0

    # Keyword extraction (filtering stopwords)
    content_words = remove_stopwords(all_words, lang=detected_lang)
    counts = Counter(content_words)
    top_kw = [{"word": word, "count": count} for word, count in counts.most_common(12)]

    return SocialBatchReport(
        platform=platform,
        total_posts=len(posts),
        total_words=total_words,
        dominant_language=detected_lang,
        avg_sentence_length=round(total_words / total_evaluated, 2),
        sentiment_distribution=sent_dist,
        avg_polarity=avg_pol,
        avg_readability_score=avg_read,
        readability_metric_name=metric_name,
        type_token_ratio=ttr,
        top_keywords=top_kw,
    )


def fetch_reddit_posts(subreddit: str = "polska", limit: int = 25) -> List[SocialPost]:
    """Fetch public post titles and selftexts from a specified subreddit via Reddit public JSON API.

    No API credentials required for read-only public feeds.

    Args:
        subreddit: Name of the subreddit (e.g. 'polska', 'python', 'europe').
        limit: Number of posts to retrieve (max 100).

    Returns:
        List of SocialPost objects.
    """
    clean_sub = subreddit.strip().lstrip("r/")
    url = f"https://www.reddit.com/r/{clean_sub}/hot.json?limit={min(100, max(1, limit))}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "WriteGenius-Academic-Analyzer/0.1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            children = data.get("data", {}).get("children", [])
            posts: List[SocialPost] = []
            for item in children:
                p_data = item.get("data", {})
                title = p_data.get("title", "")
                selftext = p_data.get("selftext", "")
                full_body = f"{title}. {selftext}".strip()
                if full_body:
                    posts.append(
                        SocialPost(
                            id=p_data.get("id", ""),
                            platform="reddit",
                            text=full_body,
                            author=p_data.get("author"),
                            score=p_data.get("score"),
                            created_at=str(p_data.get("created_utc")),
                        )
                    )
            return posts
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        # Fallback empty list on connection or rate-limit failure
        return []


def parse_x_timeline(tweets_data: List[Dict[str, Any]]) -> List[SocialPost]:
    """Parse raw X (Twitter) API v2 tweet dictionaries into standardized SocialPost items.

    Args:
        tweets_data: List of tweet dictionaries from X API v2 payload.

    Returns:
        List of SocialPost items.
    """
    posts: List[SocialPost] = []
    for t in tweets_data:
        text = t.get("text", "")
        if text:
            posts.append(
                SocialPost(
                    id=str(t.get("id", "")),
                    platform="x",
                    text=text,
                    author=t.get("author_id"),
                    score=t.get("public_metrics", {}).get("like_count"),
                    created_at=t.get("created_at"),
                )
            )
    return posts
