# Contributing to WriteGenius

Thank you for your interest in contributing to **WriteGenius**! We welcome contributions to expand linguistic capabilities for European languages.

## Getting Started

1. **Fork the Repository** on GitHub.
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/spiktokmarcin-rgb/WriteGenius.git
   cd WriteGenius
   ```
3. **Install the package in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development & Testing

Before submitting a Pull Request, run the test suite:

```bash
pytest
```

We aim for high test coverage and clean, idiomatic Python code.

## Areas for Contribution

- Adding stopword lexicons for additional European languages (e.g. Portuguese, Dutch, Czech, Greek).
- Syllable counting rules and benchmark validation against linguistic datasets.
- Lemmatization mappings.
- Enhancing sentiment lexicons.

## Pull Request Guidelines

1. Create a feature branch (`git checkout -b feature/new-language-support`).
2. Commit your changes with clear messages (`git commit -m "feat: add Czech stopwords and syllable rules"`).
3. Ensure all tests pass.
4. Push to your branch and open a PR.

## Code of Conduct

Please treat everyone with respect and empathy. We are committed to providing a friendly, safe, and welcoming environment for all contributors.
