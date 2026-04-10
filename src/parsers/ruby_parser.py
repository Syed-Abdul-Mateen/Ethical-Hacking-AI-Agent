"""
Ruby parser using regular expressions.
"""

import re
from typing import List, Dict

from src.parsers.base_parser import BaseParser, ParsedFile


class RubyParser(BaseParser):
    """Parser for Ruby source files."""

    def parse(self, file_path: str, content: str) -> ParsedFile:
        """Parse Ruby file and return ParsedFile."""
        lines = content.splitlines()
        parsed_data = {
            "requires": self._extract_requires(content),
            "methods": self._extract_methods(content),
            "sql_strings": self._extract_sql_strings(content),
            "dangerous_calls": self._extract_dangerous_calls(content),
            "classes": self._extract_classes(content),
        }
        return ParsedFile(
            file_path=file_path,
            content=content,
            lines=lines,
            language="ruby",
            parsed_data=parsed_data,
        )

    def _extract_requires(self, content: str) -> List[str]:
        """Extract require statements."""
        pattern = re.compile(r"require\s+['\"]([^'\"]+)['\"]")
        return pattern.findall(content)

    def _extract_methods(self, content: str) -> List[Dict[str, str]]:
        """Extract method definitions."""
        pattern = re.compile(r"def\s+(\w+)")
        methods = []
        for match in pattern.finditer(content):
            methods.append({"name": match.group(1), "signature": match.group(0)})
        return methods

    def _extract_sql_strings(self, content: str) -> List[str]:
        """Extract SQL strings with interpolation."""
        sql_keywords = r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b"
        pattern = re.compile(r'("[^"]*"|\'[^\']*\')', re.IGNORECASE)
        sql_strings = []
        for match in pattern.finditer(content):
            s = match.group(1)
            if re.search(sql_keywords, s, re.IGNORECASE) and ("#" in s or "?" in s):
                sql_strings.append(s)
        return sql_strings

    def _extract_dangerous_calls(self, content: str) -> List[Dict[str, str]]:
        """Extract dangerous calls like system, exec."""
        patterns = [
            (r"system\s*\([^)]*\)", "system"),
            (r"exec\s*\([^)]*\)", "exec"),
            (r"`[^`]*`", "backticks"),
            (r"IO\.popen\s*\([^)]*\)", "IO.popen"),
        ]
        dangerous = []
        for pattern, name in patterns:
            for match in re.finditer(pattern, content):
                dangerous.append({"name": name, "line": content[: match.start()].count("\n") + 1})
        return dangerous

    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names."""
        pattern = re.compile(r"class\s+(\w+)")
        return pattern.findall(content)