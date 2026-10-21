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
