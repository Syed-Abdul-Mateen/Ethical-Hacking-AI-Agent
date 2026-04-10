#!/bin/bash
# Activate virtual environment and run agent CLI

source venv/bin/activate
python3 -m src.main "$@"