from typing import Dict, Any
from .base_parser import BaseParser, ParsedFile

class SQLParser(BaseParser):
    """Parser for SQL files."""
    def parse(self, file_path) -> ParsedFile:
        return ParsedFile(file_path, content if 'content' in locals() else "", "sql")
    def get_supported_extensions(self) -> list[str]:
        return [".sql"]
