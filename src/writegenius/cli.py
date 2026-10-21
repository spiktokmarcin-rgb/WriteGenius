"""Command-line interface for WriteGenius."""

from __future__ import annotations
import sys
import argparse
from pathlib import Path
from writegenius import __version__
from writegenius.pipeline import analyze_text
from writegenius.metrics.polish_metrics import calculate_pisarek_index
from writegenius.core.text_stats import compute_text_stats
from writegenius.integrations.x_client import prepare_x_thread
from writegenius.integrations.wykop_client import format_wykop_entry, WykopClient


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for WriteGenius."""
    parser = argparse.ArgumentParser(
        prog="writegenius",
        description="WriteGenius: Multilingual Natural Language Processing & Readability Engine for European Languages",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Subcommand: analyze
    p_analyze = subparsers.add_parser("analyze", help="Full analysis report of text")
    p_analyze.add_argument("text", nargs="?", default=None, help="Input text to analyze")
    p_analyze.add_argument("-f", "--file", type=str, help="Path to text file to analyze")
    p_analyze.add_argument("-l", "--lang", type=str, default=None, help="Target language code (e.g. 'pl', 'en', 'de')")
    p_analyze.add_argument("--json", action="store_true", help="Output full report as formatted JSON")

    # Subcommand: pisarek (Polish readability)
    p_pisarek = subparsers.add_parser("pisarek", help="Calculate Polish Pisarek Readability Index")
    p_pisarek.add_argument("text", nargs="?", default=None, help="Input Polish text")
    p_pisarek.add_argument("-f", "--file", type=str, help="Path to text file")

    # Subcommand: stats
    p_stats = subparsers.add_parser("stats", help="Compute surface text statistics")
    p_stats.add_argument("text", nargs="?", default=None, help="Input text")
    p_stats.add_argument("-f", "--file", type=str, help="Path to text file")
    p_stats.add_argument("-l", "--lang", type=str, default="pl", help="Target language code")

    # Subcommand: thread-x
    p_thread = subparsers.add_parser("thread-x", help="Segment text into an X (Twitter) thread")
    p_thread.add_argument("text", nargs="?", default=None, help="Input text to segment")
    p_thread.add_argument("-f", "--file", type=str, help="Path to text file")
    p_thread.add_argument("--max-chars", type=int, default=280, help="Max characters per post (default: 280)")

    # Subcommand: draft-wykop
    p_wykop = subparsers.add_parser("draft-wykop", help="Generate formatted Wykop Mikroblog entry")
    p_wykop.add_argument("text", nargs="?", default=None, help="Input text or draft body")
    p_wykop.add_argument("-f", "--file", type=str, help="Path to text file")
    p_wykop.add_argument("--tags", type=str, default="programowanie,python,opensource", help="Comma-separated hashtags")
    p_wykop.add_argument("--preset-showcase", action="store_true", help="Print pre-written open source announcement draft")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    # Resolve text input
    input_text = ""
    if args.command == "draft-wykop" and getattr(args, "preset_showcase", False):
        pass
    elif getattr(args, "file", None):
        file_path = Path(args.file)
        if not file_path.exists():
            sys.stderr.write(f"Error: File not found: {args.file}\n")
            return 1
        input_text = file_path.read_text(encoding="utf-8")
    elif getattr(args, "text", None):
        input_text = args.text
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read()
    else:
        sys.stderr.write("Error: Please provide text via arguments, file, or stdin.\n")
        return 1

    if args.command == "analyze":
        report = analyze_text(input_text, lang=args.lang)
        if args.json:
            print(report.to_json())
        else:
            print(report.summary())
        return 0

    if args.command == "pisarek":
        res = calculate_pisarek_index(input_text)
        print(f"Indeks Pisarka (W): {res.pisarek_index}")
        print(f"Poziom trudności:  {res.pisarek_difficulty_level}")
        print(f"Odbiorca docelowy: {res.pisarek_target_audience}")
        print(f"Trudne słowa 4+:   {res.hard_words_ratio_percent}%")
        print(f"FOG (Polska):      {res.fog_polish}")
        return 0

    if args.command == "stats":
        stats = compute_text_stats(input_text, lang=args.lang)
        print(f"Characters:         {stats.character_count} (no spaces: {stats.character_count_no_spaces})")
        print(f"Words:              {stats.word_count}")
        print(f"Sentences:          {stats.sentence_count}")
        print(f"Syllables:          {stats.syllable_count}")
        print(f"Avg Sentence Len:   {stats.avg_sentence_length}")
        print(f"Avg Word Len:       {stats.avg_word_length}")
        print(f"Syllables per word: {stats.avg_syllables_per_word}")
        return 0

    if args.command == "thread-x":
        tweets = prepare_x_thread(input_text, max_chars=args.max_chars)
        print(f"--- Generated X Thread ({len(tweets)} tweets) ---")
        for i, t in enumerate(tweets, 1):
            print(f"\n[Tweet {i}/{len(tweets)} - {len(t)} chars]:\n{t}")
        return 0

    if args.command == "draft-wykop":
        if getattr(args, "preset_showcase", False) or not input_text:
            draft = WykopClient.generate_showcase_draft()
            print("--- Wykop Mikroblog Showcase Draft ---\n")
            print(draft)
            return 0
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        formatted = format_wykop_entry(input_text, tags=tags)
        print("--- Formatted Wykop Mikroblog Entry ---\n")
        print(formatted)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
