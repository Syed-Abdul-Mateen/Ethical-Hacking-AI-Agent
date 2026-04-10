# User Guide

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run the agent: `ethical-hacking-agent scan /path/to/target`
3. View reports in `reports/` directory.

## Options

- `--dynamic`: Enable dynamic testing (starts a local server).
- `--output`: Output format (html, json, markdown, pdf).
- `--config`: Custom configuration file.

## Web UI

To start the web dashboard:
```bash
export FLASK_APP=src/web_ui/app.py
flask run