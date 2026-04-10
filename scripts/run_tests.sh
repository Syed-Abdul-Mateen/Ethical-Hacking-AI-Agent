#!/bin/bash
# Run pytest with coverage

pytest --cov=src --cov-report=html tests/
echo "Tests complete. Coverage report in htmlcov/"