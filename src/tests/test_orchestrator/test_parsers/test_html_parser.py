"""
Test HTML parser.
"""

import pytest
from pathlib import Path
from src.parsers.html_parser import HTMLParser
from src.utils.config import Config


@pytest.fixture
def config(tmp_path):
    config_content = "agent:\n  name: Test\nparsers: {}\n"
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    return Config(config_file)


def test_html_parser(config, tmp_path):
    parser = HTMLParser(config)
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><body><script>alert(1)</script></body></html>")
    parsed = parser.parse(html_file)
    assert parsed is not None
    assert parsed.language == "html"
    assert len(parsed.metadata["inline_scripts"]) == 1


def test_html_parser_extracts_forms(config, tmp_path):
    parser = HTMLParser(config)
    html_file = tmp_path / "form.html"
    html_file.write_text('<html><body><form action="/login" method="POST"></form></body></html>')
    parsed = parser.parse(html_file)
    assert parsed is not None
    assert len(parsed.metadata["forms"]) == 1
    assert parsed.metadata["forms"][0]["action"] == "/login"
    assert parsed.metadata["forms"][0]["method"] == "POST"


def test_html_parser_extracts_event_handlers(config, tmp_path):
    parser = HTMLParser(config)
    html_file = tmp_path / "handlers.html"
    html_file.write_text('<html><body><div onclick="doStuff()">click</div></body></html>')
    parsed = parser.parse(html_file)
    assert parsed is not None
    assert len(parsed.metadata["event_handlers"]) == 1