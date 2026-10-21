.PHONY: help install test benchmark demo build clean

help:
	@echo "WriteGenius Development Commands:"
	@echo "  make install    Install writegenius in editable mode with dev dependencies"
	@echo "  make test       Run the complete pytest test suite"
	@echo "  make benchmark  Run corpus regression and benchmark tests"
	@echo "  make demo       Launch the interactive Streamlit Studio web app"
	@echo "  make build      Build distribution wheel and source tarball"
	@echo "  make clean      Remove build artifacts and temporary cache directories"

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]" streamlit build twine

test:
	pytest -v

benchmark:
	pytest tests/test_benchmark_corpus.py -v

demo:
	streamlit run app.py

build:
	python -m build
	twine check dist/*

clean:
	rm -rf build/ dist/ src/*.egg-info .pytest_cache/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
