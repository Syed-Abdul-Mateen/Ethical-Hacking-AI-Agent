"""Parser for PHP files."""

import re
from pathlib import Path
from typing import Optional, List, Dict

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PHPParser(BaseParser):
    """Parse PHP files, extracting variables, functions, and SQL queries."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "php"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)

        # Extract metadata using regex (simplified; in real-world, use a proper PHP parser like php-ast)
        metadata = {
            "functions": [],
            "variables": [],
            "includes": [],
            "superglobals_used": [],
            "sql_queries": [],
        }

        # Find function definitions
        func_matches = re.finditer(r'function\s+(\w+)\s*\(', content)
        for match in func_matches:
            metadata["functions"].append(match.group(1))

        # Find includes/requires
        include_matches = re.finditer(r'(include|require)(_once)?\s*["\']([^"\']+)["\']', content)
        for match in include_matches:
            metadata["includes"].append(match.group(3))

        # Find superglobals
        superglobals = ['$_GET', '$_POST', '$_REQUEST', '$_SESSION', '$_COOKIE', '$_FILES', '$_SERVER']
        for sg in superglobals:
            if sg in content:
                metadata["superglobals_used"].append(sg)

        # Simple SQL query detection
        sql_pattern = r'("|\')(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP).*?("|\')'
        sql_matches = re.finditer(sql_pattern, content, re.IGNORECASE)
        for match in sql_matches:
            metadata["sql_queries"].append(match.group(0))

        parsed.metadata = metadata

        return parsed