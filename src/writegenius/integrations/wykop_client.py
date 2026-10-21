"""Wykop API v3 integration and Mikroblog formatting for WriteGenius."""

from __future__ import annotations
import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional


def format_wykop_entry(content: str, tags: Optional[List[str]] = None) -> str:
    """Format content for Wykop Mikroblog with compliant Markdown and hashtags.

    Args:
        content: Main body text of the entry.
        tags: List of tag names without '#' prefix (e.g. ['programowanie', 'python']).

    Returns:
        Formatted entry string with appended hashtags.
    """
    clean_body = content.strip()
    if not tags:
        return clean_body

    formatted_tags = []
    for t in tags:
        clean_tag = t.strip().lstrip("#")
        if clean_tag:
            formatted_tags.append(f"#{clean_tag}")

    if not formatted_tags:
        return clean_body

    tag_line = " ".join(formatted_tags)
    return f"{clean_body}\n\n{tag_line}"


class WykopClient:
    """Client for Wykop API v3 endpoints (Mikroblog entries and community showcases)."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("WYKOP_TOKEN") or os.getenv("WYKOP_BEARER_TOKEN")
        self.api_url = "https://wykop.pl/api/v3/entries"

    def create_entry(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        adult_content: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Post a new entry to Wykop Mikroblog via API v3.

        Args:
            content: Text body of the entry.
            tags: Optional list of hashtags.
            adult_content: 18+ flag (default: False).
            dry_run: If True, returns validated payload without calling the API.

        Returns:
            API response or dry-run validation dictionary.
        """
        full_text = format_wykop_entry(content, tags=tags)
        payload = {
            "data": {
                "content": full_text,
                "adult": adult_content,
            }
        }

        if dry_run or not self.token:
            return {
                "status": "dry_run",
                "mock_id": f"mock_wykop_{abs(hash(full_text)) % 1000000}",
                "formatted_entry": full_text,
                "payload": payload,
                "token_present": bool(self.token),
            }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.token}",
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

    @staticmethod
    def generate_showcase_draft(repo_url: str = "https://github.com/spiktokmarcin-rgb/WriteGenius") -> str:
        """Generate an anti-slop, factual draft entry for the Wykop #programowanie community."""
        return (
            "Cześć Mirki spod #programowanie i #python,\n\n"
            "Większość bibliotek NLP (np. textstat czy standardowy Flesch) powstała z myślą "
            "o angielszczyźnie, gdzie słowa 3-sylabowe uznaje się za trudne. W języku polskim "
            "sama odmiana (np. 'zrobiliśmy', 'samochodami') wydłuża słowa do 4-5 sylab, "
            "co w klasycznych formułach daje na zwykłym artykule absurdalne ujemne wyniki czytelności.\n\n"
            "Stworzyłem WriteGenius - lekki (0 MB ciężkich zależności, czysty Python) silnik NLP "
            "dla języków europejskich implementujący empiryczny Indeks Pisarka (1969) "
            "ze specjalną obsługą polskich zmiękczeń sylabowych (nie-bo, wio-sna), Flesch, FOG, "
            "bogactwo leksykalne (TTR, Guiraud) oraz gotowe studio w Streamlit.\n\n"
            f"Kod i dokumentacja na GitHubie: {repo_url}\n\n"
            "#programowanie #python #opensource #nlp #naukaprogramowania"
        )
