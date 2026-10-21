<div align="center">

# WriteGenius 🧠🇪🇺

**Multilingual Natural Language Processing & Readability Engine for European Languages**

[![CI](https://github.com/spiktokmarcin-rgb/WriteGenius/actions/workflows/ci.yml/badge.svg)](https://github.com/spiktokmarcin-rgb/WriteGenius/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Supported Languages](https://img.shields.io/badge/languages-PL%20%7C%20EN%20%7C%20DE%20%7C%20FR%20%7C%20ES%20%7C%20IT%20%7C%20UK-green.svg)](#supported-languages)
[![Zero Heavy Dependencies](https://img.shields.io/badge/dependencies-zero%20heavy%20bloat-brightgreen.svg)](#architecture)

[Features](#-features) • [Installation](#-installation) • [Interactive Web Studio](#-interactive-web-studio) • [Quickstart](#-quickstart) • [Benchmarks & Empirical Data](docs/BENCHMARKS.md) • [Polish Readability & Pisarek Index](#-the-polish-readability-challenge) • [CLI](#-command-line-interface) • [DevRel Agent](#-devrel--outreach-agent) • [Publications](docs/RESEARCH_AND_CITATIONS.md) • [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

Most standard Natural Language Processing (NLP) toolkits and readability packages (such as `textstat` or generic Flesch implementations) were designed exclusively around English syllable dynamics and Anglo-Saxon morphology.

When applied to **European languages**—especially highly inflected Central and Eastern European languages like **Polish**—these tools produce fundamentally distorted results:
- In English, a word with 3 syllables is typically "complex" or "hard" (e.g., *com-pu-ter*).
- In Polish, everyday grammatical inflections regularly add 1 to 2 syllables to basic vocabulary (e.g., *zro-bi-li-by-ście* has 5 syllables).
- Treating 3-syllable Polish words as "complex" causes standard English formulas to label even simple children's fairy tales as postgraduate-level text.

**WriteGenius** solves this fundamental gap. It is an open-source, lightweight, high-performance NLP engine designed specifically for European languages, featuring first-class calibrated formulas for **Polish**, **English**, **German**, **French**, **Spanish**, **Italian**, and **Ukrainian**.

---

## ✨ Features

- **🇵🇱 First-Class Polish Readability (Indeks Pisarka 1969)**
  - Accurate implementation of Walery Pisarek's empirical formula ($W = \frac{T}{Z} + \frac{B}{T} \times 100$).
  - High-precision Polish vowel and glide syllabification (handles *i* palatalization such as *nie-bo*, *zro-bić*, *wio-sna*).
  - Polish-adapted Gunning Fog index.
- **🌍 International Readability Suite**
  - Flesch Reading Ease (with language-specific coefficients for English, German, French, and Spanish).
  - Flesch-Kincaid Grade Level, Gunning Fog Index, Coleman-Liau Index, and Automated Readability Index (ARI).
- **📊 Lexical Diversity & Vocabulary Richness**
  - Type-Token Ratio (TTR) and Root TTR (Guiraud's Index $R = \frac{V}{\sqrt{N}}$).
  - Hapax Legomena ratio (words occurring once) and content-word Lexical Density.
- **⚡ Lightweight Text Preprocessing & Diacritics Normalization**
  - Fast sentence and word tokenization with abbreviation awareness (`np.`, `m.in.`, `ul.`, `dr`, `e.g.`, `i.e.`).
  - Slavic diacritics stripping (`ą`, `ć`, `ę`, `ł`, `ń`, `ó`, `ś`, `ź`, `ż` $\to$ `a`, `c`, `e`, `l`, `n`, `o`, `s`, `z`, `z`).
  - Curated stopword sets for PL, EN, DE, FR, ES, IT, and UK.
- **💬 Explainable Sentiment & Subjectivity Analysis**
  - Rule-based sentiment scoring with negation flipping (*"nie jest dobry"* vs *"jest dobry"*) and intensifier multipliers (*"bardzo"*, *"niezwykle"*, *"very"*).
- **🚀 Zero Bloat & Instant Execution**
  - Pure Python standard library core. No gigabyte PyTorch/TensorFlow downloads required for core linguistic metrics.

---

## 📦 Installation

### From Source (Recommended)

```bash
git clone https://github.com/spiktokmarcin-rgb/WriteGenius.git
cd WriteGenius
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

---

## 🖥️ Interactive Web Studio

WriteGenius ships with a built-in Streamlit studio for instant visual text evaluation in your browser:

```bash
pip install streamlit
streamlit run app.py
```

Features included in the web interface:
- **Real-time Indeks Pisarka** with cognitive difficulty badges and target audience detection.
- **Multilingual Readability Benchmarks** (Flesch, Fog, Flesch-Kincaid, ARI).
- **Lexical Diversity & Richness meters** (TTR, Guiraud Index, Hapax Legomena, Lexical Density).
- **Automated Diagnostic Recommendations** identifying polysyllabic bottlenecks and sentence complexity.
- **Ready-to-use Presets** (Legal/Corporate Polish, News Media, Children's Story, Technical Whitepapers).

---

## 🚀 Quickstart

### 1. Unified Multilingual Analysis

```python
from writegenius import analyze_text

# Polish text sample
sample_pl = (
    "WriteGenius to nowoczesna biblioteka przetwarzania języka naturalnego. "
    "Umożliwia precyzyjną analizę czytelności i bogactwa słownictwa dla języków europejskich."
)

report = analyze_text(sample_pl)

# Human-readable executive summary
print(report.summary())

# Full structured JSON output for API pipelines
json_data = report.to_json()
```

### 2. Polish Readability Assessment (Indeks Pisarka)

```python
from writegenius import calculate_pisarek_index

legal_text = (
    "Członkowie zarządu odpowiadają solidarnie za zobowiązania spółki z o.o., "
    "jeżeli egzekucja przeciwko spółce okaże się bezskuteczna."
)

result = calculate_pisarek_index(legal_text)
print(f"Indeks Pisarka: {result.pisarek_index}")
print(f"Poziom trudności: {result.pisarek_difficulty_level}")
print(f"Trudne słowa (4+ sylaby): {result.hard_words_ratio_percent}%")
```

### 3. Surface Statistics & Vocabulary Richness

```python
from writegenius import compute_text_stats, calculate_lexical_diversity, tokenize_words

text = "The quick brown fox jumps over the lazy dog."
stats = compute_text_stats(text, lang="en")
tokens = tokenize_words(text)
diversity = calculate_lexical_diversity(tokens, lang="en")

print(f"Word count: {stats.word_count}")
print(f"Type-Token Ratio (TTR): {diversity.type_token_ratio}")
print(f"Lexical Density: {diversity.lexical_density}")
```

### 4. Exporting Production Reports (HTML & Markdown)

```python
from writegenius import analyze_text
from pathlib import Path

report = analyze_text("Twój tekst do audytu...")

# Export publication-ready HTML audit with print styles
Path("audit_report.html").write_text(report.to_html(), encoding="utf-8")

# Export clean Markdown summary
Path("audit_report.md").write_text(report.to_markdown(), encoding="utf-8")
```

### 5. Social Distribution & Threading (X / Twitter & Wykop)

```python
from writegenius import prepare_x_thread, WykopClient

# 1. Break down an article into sentence-compliant X thread chunks (<= 280 chars)
tweets = prepare_x_thread("Długi artykuł naukowy lub komunikat...", max_chars=280)
for tweet in tweets:
    print(tweet)

# 2. Format a publication draft for Wykop Mikroblog
wykop_post = WykopClient.generate_showcase_draft()
print(wykop_post)
```

### 6. Social Media Discourse Analytics (Reddit & X.com)

```python
from writegenius import fetch_reddit_posts, analyze_social_posts, parse_x_timeline

# 1. Ingest public posts from Reddit (e.g. r/polska) without requiring API keys
reddit_posts = fetch_reddit_posts(subreddit="polska", limit=20)
reddit_report = analyze_social_posts(reddit_posts, lang="pl")
print(reddit_report.summary())

# 2. Ingest and analyze a timeline of tweets from X.com API v2
tweets_payload = [{"id": "1", "text": "Exciting updates in open source European NLP."}]
x_posts = parse_x_timeline(tweets_payload)
x_report = analyze_social_posts(x_posts, lang="en")
print(x_report.summary())
```

---

## 🔬 The Polish Readability Challenge

In Polish linguistics, the standard reference method for readability is **Walery Pisarek's Index (1969)**. Pisarek proved empirically that for inflected Slavic languages, cognitive difficulty correlates with:
1. Average sentence length ($T / Z$, total words divided by total sentences).
2. The proportion of words having **4 or more syllables** ($B / T \times 100$).

$$\text{Pisarek Index } (W) = \frac{T}{Z} + \frac{B_{4+}}{T} \times 100$$

### Difficulty Scale for Polish

| Score ($W$) | Difficulty Level | Typical Target Audience |
| :--- | :--- | :--- |
| **< 18** | Bardzo łatwy | Primary school (grades 1–6), instructions |
| **18 – 25** | Łatwy | Daily press, news portals, mass communication |
| **26 – 33** | Przeciętny | Secondary education, general nonfiction |
| **34 – 41** | Trudny | Higher education, legal & academic articles |
| **$\ge$ 42** | Bardzo trudny | Official administrative jargon, doctoral theses |

WriteGenius automatically categorizes Polish text and provides automated recommendations when the proportion of 4+ syllable words exceeds cognitive thresholds.

---

## 💻 Command-Line Interface (CLI)

WriteGenius ships with a built-in CLI:

```bash
# Full analysis summary
writegenius analyze "Właściwa diagnoza niewypłacalności chroni majątek zarządu." --lang pl

# Output as JSON
writegenius analyze -f sample.txt --json

# Direct Pisarek index check
writegenius pisarek "Twój artykuł prasowy tutaj."

# Surface text statistics
writegenius stats "Krótki tekst testowy." --lang pl

# Segment an article into an X (Twitter) thread (280 chars per tweet)
writegenius thread-x "Długi tekst do podziału na wątek..." --max-chars 280

# Generate a formatted Wykop Mikroblog community draft
writegenius draft-wykop --preset-showcase

# Analyze social media feeds (e.g. Reddit r/polska or X JSON feeds)
writegenius analyze-social --platform reddit --subreddit polska --limit 20
writegenius analyze-social --platform x -f tweets.json --json
```

---

## 🌐 Supported Languages

| Language | Code | Tokenization | Syllabification | Stopwords | Readability Customization |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Polish** | `pl` | ✅ | ✅ (Diphthong aware) | ✅ | ✅ Pisarek & Polish FOG |
| **English** | `en` | ✅ | ✅ (Silent 'e' rule) | ✅ | ✅ Flesch, FKG, Fog, ARI |
| **German** | `de` | ✅ | ✅ (Umlauts) | ✅ | ✅ Amstad Flesch |
| **French** | `fr` | ✅ | ✅ (Accents) | ✅ | ✅ Kandel-Moles Flesch |
| **Spanish** | `es` | ✅ | ✅ (Tildes) | ✅ | ✅ Fernandez-Huerta |
| **Italian** | `it` | ✅ | ✅ | ✅ | ✅ Multilingual |
| **Ukrainian** | `uk` | ✅ | ✅ (Cyrillic vowels) | ✅ | ✅ Multilingual |

---

## 🧪 Testing

WriteGenius maintains a comprehensive test suite covering tokenization, linguistic edge-cases, syllable detection, and metric calculations:

```bash
pytest
```

---

## 🗺️ Roadmap

- [x] Syllable nucleus detection with Polish palatal glide handling
- [x] Indeks Pisarka & Polish-adapted FOG
- [x] Multi-lingual European stopword dictionary (7 languages)
- [x] Explainable sentiment & subjectivity with negation window
- [x] CLI entry point & JSON reporting
- [x] Export to publication-ready HTML & Markdown executive reporting
- [x] Interactive Streamlit studio with difficulty badges
- [x] Multilingual benchmark reference corpus & scale breakdown docs
- [x] Social media discourse analytics for Reddit & X.com feeds
- [x] Value-first DevRel community outreach and educational campaign agent
- [ ] Lemmatization engine for Polish (Morfologik / Polimorf integration)
- [ ] Czech and Slovak language modules
- [ ] FastText / embedding-based semantic similarity module

---

## 📣 DevRel & Outreach Agent

WriteGenius includes an automated outreach assistant (`scripts/devrel_agent.py`) designed for community education and open-source dissemination on Reddit and X:

```bash
# 1. Generate educational threads for X (segmented into <= 280 char tweets)
python scripts/devrel_agent.py --platform x --mode campaigns

# 2. Generate showcase posts for Reddit (r/Python, r/Polska)
python scripts/devrel_agent.py --platform reddit --mode campaigns

# 3. Search public Reddit discussions for relevant NLP topics
python scripts/devrel_agent.py --mode search --query "czytelność"

# 4. Draft a contextual, value-first response to an ongoing thread
python scripts/devrel_agent.py --mode reply --topic-title "Jak mierzyć czytelność tekstu w Pythonie?"
```

The agent follows an anti-spam, value-first methodology: rather than dropping plain links, it explains the underlying mathematical problems (e.g. why 3+ syllable rules break on Slavic morphology) and references WriteGenius as an open-source solution.

---

## 📚 Scientific Foundations & Publications

WriteGenius is built upon peer-reviewed empirical linguistics and quantitative stylometry. The complete research bibliography, formulas, and academic citations are documented in [docs/RESEARCH_AND_CITATIONS.md](docs/RESEARCH_AND_CITATIONS.md).

### Key References

1. **Walery Pisarek (1969)** — *Jak mierzyć czytelność tekstu* [How to measure text readability]. *Zeszyty Prasoznawcze*, 10(4), 35–46. The definitive empirical benchmark for Polish readability and 4+ syllable cognitive thresholds.
2. **Bartosz Broda, Bartłomiej Nitoń, Włodzimierz Gruszczyński, Maciej Ogrodniczuk (2014)** — *Measuring Readability of Polish Texts: A New Computational Approach*. *Proceedings of LREC 2014*, Reykjavik, Iceland, pp. 3118–3122. Foundational research on Polish syllabic nucleus detection and palatal glides.
3. **Rudolf Flesch (1948)** — *A new readability yardstick*. *Journal of Applied Psychology*, 32(3), 221–233.
4. **J. Peter Kincaid et al. (1975)** — *Derivation of new readability formulas (Automated Readability Index, Fog Count, and Flesch Reading Ease Formula)*. Chief of Naval Technical Training.
5. **Pierre Guiraud (1954)** — *Les caractères statistiques du vocabulaire: Essai de méthodologie*. Presses Universitaires de France. Mathematical formulation of Root TTR ($R = V / \sqrt{N}$).
6. **Robert Gunning (1952)** — *The Technique of Clear Writing*. McGraw-Hill.
7. **Bo Pang & Lillian Lee (2008)** — *Opinion Mining and Sentiment Analysis*. *Foundations and Trends in Information Retrieval*, 2(1–2), 1–135.

---

## 📜 Citation & Lineage

WriteGenius serves as the foundational open-source evaluation core of the **ContentGenius** initiative (in active research since 2022), aimed at demonstrating that AI-assisted content can match and surpass top-tier human authors in factual density, semantic clarity, and linguistic precision.

If you use WriteGenius in your academic research or production pipeline, please cite:

```bibtex
@software{writegenius2026,
  author    = {WriteGenius Contributors},
  title     = {WriteGenius: Multilingual Natural Language Processing & Readability Engine for European Languages},
  year      = {2026},
  url       = {https://github.com/spiktokmarcin-rgb/WriteGenius},
  note      = {Open-source evaluation engine of the ContentGenius ecosystem (est. 2022)}
}
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
