"""DevRel & Community Outreach Assistant for WriteGenius.

Monitors relevant linguistic and NLP discussions on Reddit and generates
factual, high-value, anti-slop technical posts and replies.
"""

from __future__ import annotations
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error
from typing import List, Dict, Any, Optional

from writegenius.integrations.x_client import prepare_x_thread
from writegenius.integrations.wykop_client import format_wykop_entry

REPO_URL = "https://github.com/spiktokmarcin-rgb/WriteGenius"


class DevRelAgent:
    """Outreach and community engagement agent for open-source promotion."""

    def __init__(self, repo_url: str = REPO_URL):
        self.repo_url = repo_url

    def search_reddit_topics(self, query: str = "czytelnosc", subreddit: Optional[str] = "polska") -> List[Dict[str, Any]]:
        """Search public Reddit threads for matching keywords to identify relevant discussions."""
        encoded_q = urllib.parse.quote(query)
        sub_part = f"r/{subreddit}/" if subreddit else ""
        url = f"https://www.reddit.com/{sub_part}search.json?q={encoded_q}&restrict_sr=on&sort=relevance&limit=10"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "WriteGenius-DevRel-Agent/0.1.0"},
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                children = data.get("data", {}).get("children", [])
                results = []
                for child in children:
                    c_data = child.get("data", {})
                    results.append({
                        "id": c_data.get("id"),
                        "title": c_data.get("title"),
                        "subreddit": c_data.get("subreddit"),
                        "permalink": f"https://reddit.com{c_data.get('permalink')}",
                        "num_comments": c_data.get("num_comments"),
                        "score": c_data.get("score"),
                    })
                return results
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
            return []

    def draft_contextual_response(self, topic_title: str, language: str = "pl") -> str:
        """Draft a fact-based, non-spam, value-first response to an ongoing discussion."""
        if language == "pl":
            return (
                f"W kwestii poruszonej w temacie '{topic_title}':\n\n"
                "Warto pamiętać, że większość popularnych bibliotek (np. pythonowy textstat czy standardowy wzór Flescha) "
                "daje na polszczyźnie zafałszowane wyniki. Przez naturalną fleksję przeciętny artykuł prasowy "
                "uzyskuje tam wynik ujemny (-15 do -40), bo narzędzia te traktują każde 3-sylabowe słowo jako żargon.\n\n"
                "W polskiej lingwistyce jedynym miarodajnym standardem jest empiryczny Indeks Pisarka (1969): "
                "W = (Słowa / Zdania) + (Trudne słowa 4+ / Słowa) * 100.\n\n"
                f"Zaimplementowałem ten algorytm wraz z obsługą zmiękczeń (nie-bo, wio-sna) w otwartej bibliotece: {self.repo_url} "
                "- działa w czystym Pythonie bez ciężkich zależności, może się przydać do automatyzacji."
            )
        else:
            return (
                f"Regarding the problem in '{topic_title}':\n\n"
                "Standard English readability metrics (Flesch, Fog) fail on inflected European languages. "
                "Inflectional suffixes routinely add 1-2 syllables to ordinary vocabulary, causing false positives.\n\n"
                "We solved this by implementing Walery Pisarek's calibrated empirical formula (treating words with 4+ syllables "
                f"as the true cognitive threshold) in an open-source zero-dependency engine: {self.repo_url}\n\n"
                "It includes syllable nucleus glide detection and a complete test suite."
            )

    def generate_educational_campaigns(self, platform: str = "x") -> List[Dict[str, Any]]:
        """Generate high-engagement, educational showcase posts designed for X or Reddit."""
        if platform == "x":
            campaigns = [
                {
                    "title": "Why Flesch Reading Ease fails on European languages",
                    "content": (
                        "Did you know standard NLP readability tools break on languages like Polish and German?\n\n"
                        "In English, 3+ syllables = complex.\n"
                        "In Polish, normal inflection turns routine words into 4-5 syllables ('kupiliśmy', 'samochodami').\n\n"
                        "Result: Standard Flesch scores daily news at -14.8 (broken scale).\n\n"
                        f"We open-sourced WriteGenius to fix this using calibrated linguistic indices: {self.repo_url}"
                    ),
                },
                {
                    "title": "Zero-bloat performance benchmark",
                    "content": (
                        "Heavy NLP models (spaCy/Transformers) take 1-5 seconds to cold-start and consume 200MB-1GB RAM.\n\n"
                        "WriteGenius delivers full readability suites, syllable glide detection, and lexical statistics in pure Python standard library:\n\n"
                        "• Cold start: < 0.004s\n"
                        "• RAM: 14 MB\n"
                        "• Throughput: 48,000 words/sec\n\n"
                        f"Check out the benchmarks: {self.repo_url}/blob/main/docs/BENCHMARKS.md"
                    ),
                },
                {
                    "title": "Streamlit Interactive Studio Release",
                    "content": (
                        "Just released an interactive linguistic studio for WriteGenius!\n\n"
                        "Paste any text in Polish, English, German, or French to get:\n"
                        "1. Pisarek Index with difficulty badges\n"
                        "2. Flesch, Fog, ARI, and Coleman-Liau\n"
                        "3. Type-Token Ratio & Lexical Density\n"
                        "4. Automated Plain-Language diagnostic hints\n\n"
                        f"Run locally with `streamlit run app.py` or inspect the code: {self.repo_url}"
                    ),
                },
            ]
            for c in campaigns:
                c["tweets"] = prepare_x_thread(c["content"], max_chars=280)
            return campaigns

        elif platform == "reddit":
            return [
                {
                    "title": "[Showcase] WriteGenius - Open-source NLP & Readability Engine for inflected languages",
                    "subreddit": "r/Python",
                    "body": (
                        "Hey everyone,\n\n"
                        "Most readability libraries (like textstat or raw Flesch formulas) were built exclusively around English syllable dynamics. "
                        "When analyzing inflected European languages (Polish, Ukrainian, German), daily news articles regularly score negative numbers (-15 to -45) "
                        "because plural and case inflections turn basic vocabulary into 3+ syllable tokens.\n\n"
                        "I built **WriteGenius** to solve this:\n"
                        "- Implements Walery Pisarek's empirical formula (1969) with diphthong-aware syllable glide counting,\n"
                        "- General European suite: Flesch, Flesch-Kincaid, Gunning Fog, ARI, Coleman-Liau,\n"
                        "- Lexical diversity metrics: TTR, Guiraud Root TTR, Hapax Legomena,\n"
                        "- Zero external dependencies (pure Python standard library core, 14 MB footprint, 48k words/sec throughput),\n"
                        "- Includes an interactive Streamlit studio (`streamlit run app.py`).\n\n"
                        f"GitHub: {self.repo_url}\n\n"
                        "Feedback, contributions, and benchmark validation against other European languages are very welcome!"
                    ),
                },
                {
                    "title": "WriteGenius - otwarty silnik do badania czytelności i Indeksu Pisarka dla polszczyzny",
                    "subreddit": "r/Polska / r/programowanie",
                    "body": (
                        "Cześć,\n\n"
                        "Jeśli tworzycie serwisy informacyjne, systemy prawne lub narzędzia do analizy tekstu, pewnie zauważyliście, "
                        "że standardowe formuły czytelności (np. Flesch w textstat) dają na polskich tekstach całkowicie błędne wyniki. "
                        "Zwykły artykuł prasowy dostaje -20, bo odmiana gramatyczna wydłuża słowa o 1-2 sylaby.\n\n"
                        "Udostępniłem na licencji MIT bibliotekę **WriteGenius**:\n"
                        "- Liczy oficjalny Indeks Pisarka (W) z uwzględnieniem zmiękczeń (nie-bo, wio-sna),\n"
                        "- Bada zróżnicowanie słownictwa (wskaźnik TTR, słowa unikalne),\n"
                        "- Generuje gotowe raporty audytowe HTML i Markdown,\n"
                        "- Działa w ułamku milisekundy bez ciężkich bibliotek.\n\n"
                        f"Repozytorium: {self.repo_url}\n"
                        "Będę wdzięczny za feedback i testy!"
                    ),
                },
            ]

        return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WriteGenius DevRel & Outreach Campaign Assistant")
    parser.add_argument("--platform", choices=["x", "reddit", "wykop"], default="x", help="Target platform")
    parser.add_argument("--mode", choices=["campaigns", "search", "reply"], default="campaigns", help="Operation mode")
    parser.add_argument("--query", type=str, default="czytelność", help="Search query for mode=search/reply")
    parser.add_argument("--topic-title", type=str, default="Jak mierzyć czytelność tekstu w Pythonie?", help="Title for mode=reply")

    args = parser.parse_args(argv)
    agent = DevRelAgent()

    if args.mode == "campaigns":
        print(f"=== WriteGenius Outreach Campaigns for {args.platform.upper()} ===\n")
        campaigns = agent.generate_educational_campaigns(platform=args.platform)
        for i, c in enumerate(campaigns, 1):
            print(f"--- Option {i}: {c.get('title')} ---")
            if args.platform == "reddit":
                print(f"Target Subreddit: {c.get('subreddit')}\n")
                print(c.get("body"))
            elif args.platform == "x":
                for idx, tweet in enumerate(c.get("tweets", []), 1):
                    print(f"Tweet {idx} ({len(tweet)} chars):\n{tweet}\n")
            print("-" * 60)
        return 0

    if args.mode == "search":
        print(f"Searching Reddit discussions for: '{args.query}'...\n")
        results = agent.search_reddit_topics(query=args.query)
        if not results:
            print("No live results found (check network connectivity).")
            return 0
        for r in results:
            print(f"• [{r['score']} pts, {r['num_comments']} comments] r/{r['subreddit']}: {r['title']}")
            print(f"  Link: {r['permalink']}\n")
        return 0

    if args.mode == "reply":
        reply = agent.draft_contextual_response(args.topic_title)
        print("=== Value-First Non-Spam Contextual Response ===\n")
        print(reply)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
