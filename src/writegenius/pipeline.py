"""Unified text analysis pipeline."""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

from writegenius.core.tokenizers import tokenize_words, tokenize_sentences
from writegenius.core.text_stats import TextStatistics, compute_text_stats
from writegenius.nlp.normalizer import detect_language_heuristic
from writegenius.nlp.sentiment import SentimentResult, analyze_sentiment
from writegenius.metrics.readability import ReadabilityScores, compute_readability_suite
from writegenius.metrics.polish_metrics import PolishReadabilityResult, calculate_pisarek_index
from writegenius.metrics.lexical_diversity import LexicalDiversityResult, calculate_lexical_diversity


@dataclass
class TextAnalysisReport:
    """Comprehensive analysis report generated for a text."""
    language: str
    statistics: TextStatistics
    lexical_diversity: LexicalDiversityResult
    readability: ReadabilityScores
    polish_metrics: Optional[PolishReadabilityResult]
    sentiment: SentimentResult
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to serializable dictionary."""
        return {
            "language": self.language,
            "statistics": self.statistics.to_dict(),
            "lexical_diversity": self.lexical_diversity.to_dict(),
            "readability": self.readability.to_dict(),
            "polish_metrics": self.polish_metrics.to_dict() if self.polish_metrics else None,
            "sentiment": self.sentiment.to_dict(),
            "recommendations": self.recommendations,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def summary(self) -> str:
        """Produce an executive human-readable summary."""
        lines = [
            "=" * 60,
            f" WriteGenius Text Analysis Report (Language: {self.language.upper()})",
            "=" * 60,
            f"Words: {self.statistics.word_count} | Sentences: {self.statistics.sentence_count} | Syllables: {self.statistics.syllable_count}",
            f"Avg Sentence Length: {self.statistics.avg_sentence_length} words | Avg Word Length: {self.statistics.avg_word_length} chars",
            f"Vocabulary Richness (TTR): {self.lexical_diversity.type_token_ratio} | Lexical Density: {self.lexical_diversity.lexical_density}",
            "-" * 60,
        ]

        if self.language == "pl" and self.polish_metrics:
            lines.extend([
                f"Indeks Pisarka (W): {self.polish_metrics.pisarek_index}",
                f"Poziom trudności: {self.polish_metrics.pisarek_difficulty_level}",
                f"Odbiorca docelowy: {self.polish_metrics.pisarek_target_audience}",
                f"Trudne słowa (4+ sylaby): {self.polish_metrics.hard_words_ratio_percent}%",
                f"FOG (adaptacja polska): {self.polish_metrics.fog_polish}",
                "-" * 60,
            ])

        lines.extend([
            f"Flesch Reading Ease: {self.readability.flesch_reading_ease}",
            f"Gunning Fog: {self.readability.gunning_fog}",
            f"Flesch-Kincaid Grade: {self.readability.flesch_kincaid_grade}",
            "-" * 60,
            f"Sentiment: {self.sentiment.label.upper()} (Polarity: {self.sentiment.polarity}, Subjectivity: {self.sentiment.subjectivity})",
        ])

        if self.recommendations:
            lines.append("-" * 60)
            lines.append("Recommendations:")
            for rec in self.recommendations:
                lines.append(f" • {rec}")

        lines.append("=" * 60)
        return "\n".join(lines)

    def to_markdown(self) -> str:
        """Generate a structured GitHub-flavored Markdown audit report."""
        md = [
            f"# Linguistic Audit Report ({self.language.upper()})",
            "",
            "## Surface Statistics",
            f"- **Word Count:** {self.statistics.word_count}",
            f"- **Sentence Count:** {self.statistics.sentence_count}",
            f"- **Total Syllables:** {self.statistics.syllable_count}",
            f"- **Average Sentence Length:** {self.statistics.avg_sentence_length} words",
            f"- **Average Word Length:** {self.statistics.avg_word_length} characters",
            f"- **Average Syllables Per Word:** {self.statistics.avg_syllables_per_word}",
            "",
        ]

        if self.language == "pl" and self.polish_metrics:
            md.extend([
                "## Polish Readability (Indeks Pisarka 1969)",
                f"- **Pisarek Index (W):** `{self.polish_metrics.pisarek_index}`",
                f"- **Difficulty Level:** {self.polish_metrics.pisarek_difficulty_level}",
                f"- **Target Audience:** {self.polish_metrics.pisarek_target_audience}",
                f"- **Hard Words (4+ syllables):** {self.polish_metrics.hard_words_ratio_percent}%",
                f"- **Adapted FOG:** {self.polish_metrics.fog_polish}",
                "",
            ])

        md.extend([
            "## International Readability Benchmarks",
            "| Metric | Score |",
            "| :--- | :---: |",
            f"| Flesch Reading Ease | {self.readability.flesch_reading_ease} |",
            f"| Gunning Fog Index | {self.readability.gunning_fog} |",
            f"| Flesch-Kincaid Grade | {self.readability.flesch_kincaid_grade} |",
            f"| Automated Readability Index (ARI) | {self.readability.automated_readability_index} |",
            f"| Coleman-Liau Index | {self.readability.coleman_liau_index} |",
            "",
            "## Lexical Richness & Vocabulary",
            f"- **Type-Token Ratio (TTR):** {self.lexical_diversity.type_token_ratio}",
            f"- **Root TTR (Guiraud Index):** {self.lexical_diversity.root_ttr}",
            f"- **Hapax Legomena Ratio:** {self.lexical_diversity.hapax_ratio}",
            f"- **Lexical Density:** {self.lexical_diversity.lexical_density}",
            "",
            "## Sentiment & Subjectivity",
            f"- **Classification:** `{self.sentiment.label.upper()}`",
            f"- **Polarity:** {self.sentiment.polarity} (-1.0 to +1.0)",
            f"- **Subjectivity:** {self.sentiment.subjectivity} (0.0 to 1.0)",
            "",
        ])

        if self.recommendations:
            md.append("## Diagnostic Recommendations")
            for rec in self.recommendations:
                md.append(f"- {rec}")
            md.append("")

        return "\n".join(md)

    def to_html(self, title: str = "WriteGenius Linguistic Audit Report") -> str:
        """Generate a self-contained, publication-ready HTML report."""
        pisarek_section = ""
        if self.language == "pl" and self.polish_metrics:
            p = self.polish_metrics
            pisarek_section = f"""
            <div class="card">
                <h2>Indeks Pisarka (Oficjalny polski wzorzec czytelności)</h2>
                <div class="metric-grid">
                    <div class="metric-item">
                        <span class="label">Indeks Pisarka (W)</span>
                        <span class="val highlight">{p.pisarek_index}</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">Poziom trudności</span>
                        <span class="val">{p.pisarek_difficulty_level}</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">Słowa 4+ sylaby</span>
                        <span class="val">{p.hard_words_ratio_percent}%</span>
                    </div>
                    <div class="metric-item">
                        <span class="label">Adaptowany FOG</span>
                        <span class="val">{p.fog_polish}</span>
                    </div>
                </div>
                <p class="meta">Odbiorca docelowy: <strong>{p.pisarek_target_audience}</strong></p>
            </div>
            """

        recs_section = ""
        if self.recommendations:
            items = "".join(f"<li>{r}</li>" for r in self.recommendations)
            recs_section = f"""
            <div class="card recommendations">
                <h2>Rekomendacje diagnostyczne</h2>
                <ul>{items}</ul>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="{self.language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #111827;
        background: #f9fafb;
        margin: 0;
        padding: 40px 20px;
        line-height: 1.5;
    }}
    .container {{
        max-width: 860px;
        margin: 0 auto;
        background: #ffffff;
        padding: 36px 44px;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    header {{
        border-bottom: 2px solid #111827;
        padding-bottom: 16px;
        margin-bottom: 24px;
    }}
    h1 {{
        font-size: 24px;
        margin: 0 0 6px 0;
        font-weight: 700;
        letter-spacing: -0.01em;
    }}
    .meta-subtitle {{
        color: #6b7280;
        font-size: 14px;
        margin: 0;
    }}
    .card {{
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 20px 24px;
        margin-bottom: 20px;
        background: #ffffff;
    }}
    h2 {{
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #374151;
        margin: 0 0 16px 0;
        border-bottom: 1px solid #f3f4f6;
        padding-bottom: 8px;
    }}
    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
    }}
    .metric-item {{
        display: flex;
        flex-direction: column;
    }}
    .label {{
        font-size: 12px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .val {{
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin-top: 2px;
    }}
    .val.highlight {{
        color: #b45309;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }}
    th, td {{
        padding: 10px 14px;
        text-align: left;
        border-bottom: 1px solid #e5e7eb;
    }}
    th {{
        background: #f9fafb;
        font-weight: 600;
        color: #374151;
    }}
    .recommendations {{
        border-left: 4px solid #f59e0b;
        background: #fffbeb;
    }}
    .recommendations ul {{
        margin: 0;
        padding-left: 20px;
        color: #92400e;
    }}
    .meta {{
        font-size: 13px;
        color: #4b5563;
        margin-top: 12px;
        margin-bottom: 0;
    }}
    @media print {{
        body {{ background: #fff; padding: 0; }}
        .container {{ border: none; box-shadow: none; padding: 0; }}
    }}
</style>
</head>
<body>
<div class="container">
    <header>
        <h1>{title}</h1>
        <p class="meta-subtitle">Język: <strong>{self.language.upper()}</strong> | Silnik: WriteGenius 0.1.0 (ContentGenius Ecosystem)</p>
    </header>

    <div class="card">
        <h2>Statystyka powierzchniowa tekstu</h2>
        <div class="metric-grid">
            <div class="metric-item">
                <span class="label">Słowa</span>
                <span class="val">{self.statistics.word_count}</span>
            </div>
            <div class="metric-item">
                <span class="label">Zdania</span>
                <span class="val">{self.statistics.sentence_count}</span>
            </div>
            <div class="metric-item">
                <span class="label">Średnia dł. zdania</span>
                <span class="val">{self.statistics.avg_sentence_length} słów</span>
            </div>
            <div class="metric-item">
                <span class="label">Średnia dł. słowa</span>
                <span class="val">{self.statistics.avg_word_length} znaków</span>
            </div>
        </div>
    </div>

    {pisarek_section}

    <div class="card">
        <h2>Międzynarodowe metryki czytelności</h2>
        <table>
            <thead>
                <tr>
                    <th>Metryka</th>
                    <th>Wartość</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Flesch Reading Ease</td>
                    <td><strong>{self.readability.flesch_reading_ease}</strong></td>
                </tr>
                <tr>
                    <td>Gunning Fog Index</td>
                    <td><strong>{self.readability.gunning_fog}</strong></td>
                </tr>
                <tr>
                    <td>Flesch-Kincaid Grade Level</td>
                    <td><strong>{self.readability.flesch_kincaid_grade}</strong></td>
                </tr>
                <tr>
                    <td>Automated Readability Index (ARI)</td>
                    <td><strong>{self.readability.automated_readability_index}</strong></td>
                </tr>
                <tr>
                    <td>Coleman-Liau Index</td>
                    <td><strong>{self.readability.coleman_liau_index}</strong></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="card">
        <h2>Bogactwo leksykalne & Sentyment</h2>
        <div class="metric-grid">
            <div class="metric-item">
                <span class="label">Type-Token Ratio (TTR)</span>
                <span class="val">{self.lexical_diversity.type_token_ratio}</span>
            </div>
            <div class="metric-item">
                <span class="label">Indeks Guirauda (Root TTR)</span>
                <span class="val">{self.lexical_diversity.root_ttr}</span>
            </div>
            <div class="metric-item">
                <span class="label">Gęstość leksykalna</span>
                <span class="val">{self.lexical_diversity.lexical_density}</span>
            </div>
            <div class="metric-item">
                <span class="label">Sentyment</span>
                <span class="val">{self.sentiment.label.upper()} ({self.sentiment.polarity})</span>
            </div>
        </div>
    </div>

    {recs_section}
</div>
</body>
</html>"""


def analyze_text(text: str, lang: Optional[str] = None) -> TextAnalysisReport:
    """Analyze a text through the complete WriteGenius NLP & Readability pipeline.

    Args:
        text: Input text string.
        lang: Target language code ('pl', 'en', 'de', etc.). If None, auto-detected.

    Returns:
        TextAnalysisReport dataclass.
    """
    detected_lang = lang or detect_language_heuristic(text)
    words = tokenize_words(text)

    # 1. Surface text statistics
    stats = compute_text_stats(text, lang=detected_lang)

    # 2. Lexical diversity
    lexical = calculate_lexical_diversity(words, lang=detected_lang)

    # 3. Readability suite
    readability = compute_readability_suite(text, lang=detected_lang)

    # 4. Polish-specific metrics
    polish_metrics = None
    if detected_lang == "pl":
        polish_metrics = calculate_pisarek_index(text)

    # 5. Sentiment analysis
    sentiment = analyze_sentiment(text, lang=detected_lang)

    # 6. Actionable recommendations
    recommendations: List[str] = []
    if stats.avg_sentence_length > 20.0:
        recommendations.append(
            f"Average sentence length is {stats.avg_sentence_length} words. Consider splitting sentences to improve clarity."
        )

    if detected_lang == "pl" and polish_metrics:
        if polish_metrics.hard_words_ratio_percent > 18.0:
            recommendations.append(
                f"High proportion of 4+ syllable words ({polish_metrics.hard_words_ratio_percent}%). Replace complex words with simpler synonyms."
            )
        if polish_metrics.pisarek_index > 34.0:
            recommendations.append(
                f"Pisarek index is {polish_metrics.pisarek_index} ({polish_metrics.pisarek_difficulty_level}). High cognitive load for average readers."
            )
    else:
        if stats.avg_syllables_per_word > 1.8:
            recommendations.append(
                f"High syllable density ({stats.avg_syllables_per_word} syllables/word). Consider using shorter vocabulary."
            )

    if lexical.type_token_ratio < 0.35 and stats.word_count > 50:
        recommendations.append(
            f"Low lexical variety (TTR: {lexical.type_token_ratio}). Text contains high vocabulary repetition."
        )

    return TextAnalysisReport(
        language=detected_lang,
        statistics=stats,
        lexical_diversity=lexical,
        readability=readability,
        polish_metrics=polish_metrics,
        sentiment=sentiment,
        recommendations=recommendations,
    )
