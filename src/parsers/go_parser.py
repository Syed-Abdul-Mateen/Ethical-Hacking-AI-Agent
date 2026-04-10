"""
Go parser using regular expressions.
"""

import re
from typing import List, Dict

from src.parsers.base_parser import BaseParser, ParsedFile


class GoParser(BaseParser):
    """Parser for Go source files."""

    def parse(self, file_path: str, content: str) -> ParsedFile:
        """Parse Go file and return ParsedFile."""
        lines = content.splitlines()
        parsed_data = {
            "imports": self._extract_imports(content),
            "functions": self._extract_functions(content),
            "sql_strings": self._extract_sql_strings(content),
            "dangerous_calls": self._extract_dangerous_calls(content),
            "structs": self._extract_structs(content),
        }
        return ParsedFile(
            file_path=file_path,
            content=content,
            lines=lines,
            language="go",
            parsed_data=parsed_data,
        )

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements."""
        # Simple: import "path" or import ( "path" )
        pattern = re.compile(r'import\s+(["\w\./]+)')
        return pattern.findall(content)

    def _extract_functions(self, content: str) -> List[Dict[str, str]]:
        """Extract function definitions."""
        pattern = re.compile(r"func\s+(\w+)\s*\([^)]*\)\s*[^{]*{")
        functions = []
        for match in pattern.finditer(content):
            functions.append({"name": match.group(1), "signature": match.group(0)})
        return functions

    def _extract_sql_strings(self, content: str) -> List[str]:
        """Extract SQL strings with concatenation."""
        sql_keywords = r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\b"
        pattern = re.compile(r'("[^"]*"|`[^`]*`)', re.IGNORECASE)
        sql_strings = []
        for match in pattern.finditer(content):
            s = match.group(1)
            if re.search(sql_keywords, s, re.IGNORECASE) and ("+" in s or "$" in s or "?" in s):
                sql_strings.append(s)
        return sql_strings

    def _extract_dangerous_calls(self, content: str) -> List[Dict[str, str]]:
        """Extract dangerous calls like exec.Command."""
        patterns = [
            (r"exec\.Command\s*\(", "exec.Command"),
            (r"os\.Exec\s*\(", "os.Exec"),
            (r"syscall\.Exec\s*\(", "syscall.Exec"),
        ]
        dangerous = []
        for pattern, name in patterns:
            for match in re.finditer(pattern, content):
                dangerous.append({"name": name, "line": content[: match.start()].count("\n") + 1})
        return dangerous

    def _extract_structs(self, content: str) -> List[str]:
        """Extract struct names."""
        pattern = re.compile(r"type\s+(\w+)\s+struct")
        return pattern.findall(content)