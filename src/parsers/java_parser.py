"""
Java parser using regular expressions to extract code structures.
"""

import re
from typing import Dict, List, Optional

from src.parsers.base_parser import BaseParser, ParsedFile


class JavaParser(BaseParser):
    """Parser for Java source files."""

    def parse(self, file_path: str, content: str) -> ParsedFile:
        """
        Parse a Java file and return a ParsedFile object.

        Args:
            file_path: Path to the file.
            content: Raw content of the file.

        Returns:
            ParsedFile containing extracted data.
        """
        lines = content.splitlines()
        parsed_data = {
            "imports": self._extract_imports(content),
            "methods": self._extract_methods(content),
            "sql_strings": self._extract_sql_strings(content),
            "dangerous_calls": self._extract_dangerous_calls(content),
            "classes": self._extract_classes(content),
        }
        return ParsedFile(
            file_path=file_path,
            content=content,
            lines=lines,
            language="java",
            parsed_data=parsed_data,
        )

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        pattern = re.compile(r"import\s+([\w\.\*]+);")
        return pattern.findall(content)

    def _extract_methods(self, content: str) -> List[Dict[str, str]]:
        """Extract method signatures."""
        # Simple regex to find method declarations (ignores annotations, modifiers)
        pattern = re.compile(
            r"(?:public|private|protected)?\s+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+\w+)?\s*{"
        )
        methods = []
        for match in pattern.finditer(content):
            methods.append({"name": match.group(1), "signature": match.group(0)})
        return methods

    def _extract_sql_strings(self, content: str) -> List[str]:
        """Extract SQL strings that are concatenated."""
        # Look for strings containing SQL keywords with concatenation
        sql_keywords = r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b"
        pattern = re.compile(
            r'("[^"]*"|\'[^\']*\')', re.IGNORECASE
        )
        sql_strings = []
        for match in pattern.finditer(content):
            s = match.group(1)
            if re.search(sql_keywords, s, re.IGNORECASE):
                # Check if the string contains concatenation or variable placeholders
                if "+" in s or "?" in s:
                    sql_strings.append(s)
        return sql_strings

    def _extract_dangerous_calls(self, content: str) -> List[Dict[str, str]]:
        """Extract dangerous method calls like Runtime.exec."""
        patterns = [
            (r"Runtime\.getRuntime\(\)\.exec\(", "Runtime.exec"),
            (r"ProcessBuilder\s*\([^)]*\)", "ProcessBuilder"),
            (r"java\.lang\.reflect\.Method\.invoke\(", "Reflection.invoke"),
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