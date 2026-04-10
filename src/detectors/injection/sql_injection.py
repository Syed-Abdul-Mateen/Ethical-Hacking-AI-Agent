"""Detect potential SQL injection vulnerabilities."""

import re
from pathlib import Path
from typing import List, Dict, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.parsers.base_parser import ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SqlInjectionDetector(BaseDetector):
    """
    Detects SQL injection patterns:
    - String concatenation with user input
    - Raw SQL queries with variable interpolation
    - Dynamic queries in ORM contexts (e.g., raw SQL in Django, SQLAlchemy)
    """

    # Dangerous patterns: concatenation or interpolation
    SQL_PATTERNS = [
        r'("|\')\s*\+\s*\w+\s*\+\s*("|\')',               # "..." + var + "..."
        r'f("|\')(.*?\{.*?\}.*?)("|\')',                 # f"...{var}..."
        r'\$\w+\s*\.\s*["\']',                            # $var."..."
        r'\.\s*concat\s*\(',                              # .concat(
        r'String\.format\(.*?%s',                         # Python %s formatting
        r'%s',                                             # %s
    ]

    # Keywords that indicate SQL query building
    SQL_KEYWORDS = [
        "SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP",
        "FROM", "WHERE", "JOIN", "ORDER BY", "GROUP BY", "UNION"
    ]

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []

        for file_path, parsed in parsed_data.items():
            # Only run on languages that commonly interact with databases
            if parsed.language not in ("php", "python", "java", "csharp", "javascript", "ruby", "go"):
                continue

            for line_num, line in enumerate(parsed.lines, start=1):
                # Look for SQL keywords in the line (case-insensitive)
                has_sql_keyword = any(keyword.lower() in line.lower() for keyword in self.SQL_KEYWORDS)

                if not has_sql_keyword:
                    continue

                # Check if line contains dangerous pattern
                dangerous = False
                for pattern in self.SQL_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        dangerous = True
                        break

                # Additional heuristic: look for "query" or "sql" in variable names + concatenation
                if re.search(r'(query|sql|stmt)\s*=\s*.*?\+', line, re.IGNORECASE):
                    dangerous = True

                if dangerous:
                    snippet = parsed.get_snippet(line_num, context_lines=2)
                    finding = Finding(
                        title="Potential SQL Injection",
                        description="A SQL query appears to be constructed using string concatenation or interpolation with user-controlled data. This can lead to SQL injection if the input is not properly sanitized.",
                        severity="high",
                        file_path=file_path,
                        line_start=line_num,
                        code_snippet=snippet,
                        remediation="Use parameterized queries or prepared statements instead of string concatenation. Escape user inputs if dynamic SQL is unavoidable.",
                        cwe_id="CWE-89",
                    )
                    findings.append(finding)

        return findings