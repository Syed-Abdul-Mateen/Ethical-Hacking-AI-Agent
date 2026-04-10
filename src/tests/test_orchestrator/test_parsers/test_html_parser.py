"""
Test HTML parser.
"""

import pytest
from src.parsers.html_parser import HTMLParser


def test_html_parser():
    parser = HTMLParser()
    content = "<html><body><script>alert(1)</script></body></html>"
    parsed = parser.parse("test.html", content)
    assert parsed.language == "html"
    assert "scripts" in parsed.parsed_data
    assert len(parsed.parsed_data["scripts"]) == 1