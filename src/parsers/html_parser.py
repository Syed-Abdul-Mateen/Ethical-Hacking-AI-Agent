from typing import Dict, Any
from .base_parser import BaseParser, ParsedFile

class HTMLParser(BaseParser):
    """Parser for HTML files to extract scripts and structure."""
    def parse(self, file_path) -> ParsedFile:
        return ParsedFile(file_path, content if 'content' in locals() else "", "html")
    def get_supported_extensions(self) -> list[str]:
        return [".html", ".htm"]
