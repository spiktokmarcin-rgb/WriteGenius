"""Example: Multi-lingual text analysis with WriteGenius."""

from writegenius import analyze_text

def main():
    english_sample = (
        "WriteGenius provides accurate linguistic evaluation and readability scoring "
        "tailored for European languages. It features fast tokenizers, syllable counters, "
        "and explainable sentiment scoring."
    )

    print("--- Analyzing English Text ---")
    report = analyze_text(english_sample, lang="en")
    print(report.summary())

if __name__ == "__main__":
    main()
