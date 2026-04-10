# Developer Guide

Welcome to the Ethical Hacking AI Agent project. This guide outlines how to set up the development environment, run tests, and contribute to the codebase.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo_url>
   cd ethical_hacking_ai_agent
   ```

2. **Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install as Editable:**
   ```bash
   pip install -e .
   ```

## Running Tests

We use `pytest` for all unit and integration tests.
Execute tests from the root directory:
```bash
./scripts/run_tests.sh
```

## Adding a New Detector

1. Add your detector to the appropriate subfolder in `src/detectors/`.
2. Inherit from `BaseDetector` located in `src/detectors/base_detector.py`.
3. Implement the abstract methods.
4. Add unit tests in `tests/test_detectors/`.
5. Update `config/detectors_config.yaml` to include your new detector.

## Coding Standards

- Must include type hints (`typing` module).
- Follow PEP-8 styling. No emojis allowed.
- Write Google-style or reStructuredText docstrings for all modules, classes, and major functions.
- Maintain isolated, modular components.
