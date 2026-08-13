# CGSBS – Context-Guided Semantic Beam Search
# ----------------------------------------
# Common targets for development, demo, and packaging.

.PHONY: help install install-dev install-all \
        demo demo-renal demo-vision demo-foot \
        test lint format clean dist \
        tree

PYTHON   ?= python3
PIP      ?= pip
PACKAGE  := cgsbs
SRC      := src
NOTES    := note_renal_metformin note_vision note_foot

help:
	@echo ""
	@echo "CGSBS – Context-Guided Semantic Beam Search"
	@echo "==========================================="
	@echo ""
	@echo "Setup"
	@echo "  make install        Install package (editable) + core deps"
	@echo "  make install-dev    Install with development tools"
	@echo "  make install-all    Install full optional stack"
	@echo ""
	@echo "Demo"
	@echo "  make demo           Run primary renal + metformin demo"
	@echo "  make demo-renal     Same as demo"
	@echo "  make demo-vision    Ophthalmic context (retinopathy path)"
	@echo "  make demo-foot      Neuropathic / foot-ulcer context"
	@echo "  make demo-all       Run all three demonstration notes"
	@echo ""
	@echo "Quality"
	@echo "  make test           Run unit tests"
	@echo "  make lint           Ruff + mypy"
	@echo "  make format         Black + Ruff --fix"
	@echo ""
	@echo "Misc"
	@echo "  make clean          Remove build/cache artifacts"
	@echo "  make dist           Build sdist + wheel"
	@echo "  make tree           Show project structure"
	@echo ""

# ------------------------------------------------------------------
# Installation
# ------------------------------------------------------------------

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

install-all:
	$(PIP) install -e ".[all,dev]"

# ------------------------------------------------------------------
# Demonstrations
# ------------------------------------------------------------------

demo: demo-renal

demo-renal:
	@echo ">>> Running renal + metformin context demo"
	PYTHONPATH=$(SRC) $(PYTHON) -m $(PACKAGE).demo --note note_renal_metformin

demo-vision:
	@echo ">>> Running ophthalmic (blurred vision) context demo"
	PYTHONPATH=$(SRC) $(PYTHON) -m $(PACKAGE).demo --note note_vision

demo-foot:
	@echo ">>> Running neuropathic / foot-ulcer context demo"
	PYTHONPATH=$(SRC) $(PYTHON) -m $(PACKAGE).demo --note note_foot

demo-all: demo-renal demo-vision demo-foot

# ------------------------------------------------------------------
# Quality / Tests
# ------------------------------------------------------------------

test:
	PYTHONPATH=$(SRC) $(PYTHON) -m pytest tests/ -v

lint:
	@echo ">>> Ruff"
	ruff check $(SRC) tests
	@echo ">>> mypy"
	mypy $(SRC) || true

format:
	black $(SRC) tests
	ruff check --fix $(SRC) tests

# ------------------------------------------------------------------
# Build / Clean
# ------------------------------------------------------------------

dist:
	$(PYTHON) -m build

clean:
	rm -rf build/ dist/ *.egg-info/ .eggs/
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf src/*.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -f examples/result_*.ttl

tree:
	@find . -type f \
		-not -path './.git/*' \
		-not -path './.venv/*' \
		-not -path '*/__pycache__/*' \
		-not -path './build/*' \
		-not -path './dist/*' \
		-not -path '*.egg-info/*' \
		| sort
