"""Social platform integrations (X / Twitter, Wykop, and Reddit analytics)."""

from writegenius.integrations.x_client import XClient, prepare_x_thread
from writegenius.integrations.wykop_client import WykopClient, format_wykop_entry
from writegenius.integrations.social_analyzer import (
    SocialPost,
    SocialBatchReport,
    analyze_social_posts,
    fetch_reddit_posts,
    parse_x_timeline,
)

__all__ = [
    "XClient",
    "prepare_x_thread",
    "WykopClient",
    "format_wykop_entry",
    "SocialPost",
    "SocialBatchReport",
    "analyze_social_posts",
    "fetch_reddit_posts",
    "parse_x_timeline",
]
