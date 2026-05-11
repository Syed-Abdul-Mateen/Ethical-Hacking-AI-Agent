"""Parser for SQL files to extract queries, procedures, and dynamic parameters."""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SQLParser(BaseParser):
    """Parse SQL files extracting tables, procedures, grants, and dynamic constructs."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "sql"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)

        metadata: Dict[str, Any] = {
            "tables_referenced": [],
            "procedures": [],
            "grants": [],
            "dynamic_sql": [],
            "dangerous_operations": [],
            "comments": [],
        }

        # Extract table names from SELECT / INSERT / UPDATE / DELETE statements
        for match in re.finditer(
            r'(?:FROM|JOIN|INTO|UPDATE)\s+[`"\']?(\w+)[`"\']?',
            content, re.IGNORECASE
        ):
            table = match.group(1).upper()
            if table not in metadata["tables_referenced"]:
                metadata["tables_referenced"].append(table)

        # Extract stored procedure / function definitions
        for match in re.finditer(
            r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:PROCEDURE|FUNCTION)\s+[`"\']?(\w+)',
            content, re.IGNORECASE
        ):
            metadata["procedures"].append({
                "name": match.group(1),
                "line": content[:match.start()].count("\n") + 1,
            })

        # Extract GRANT statements (privilege escalation risks)
        for match in re.finditer(
            r'GRANT\s+(.+?)\s+ON\s+(.+?)\s+TO\s+(.+?)(?:;|$)',
            content, re.IGNORECASE
        ):
            metadata["grants"].append({
                "privilege": match.group(1).strip(),
                "target": match.group(2).strip(),
                "grantee": match.group(3).strip(),
                "line": content[:match.start()].count("\n") + 1,
            })

        # Detect dynamic SQL (EXEC/EXECUTE with string concat)
        for match in re.finditer(
            r'(?:EXEC(?:UTE)?)\s*\(\s*[\'"]?.*?\+.*?\)',
            content, re.IGNORECASE | re.DOTALL
        ):
            metadata["dynamic_sql"].append({
                "snippet": match.group(0)[:100],
                "line": content[:match.start()].count("\n") + 1,
            })

        # Detect CONCAT in WHERE clauses (potential injection)
        for match in re.finditer(
            r'WHERE\s+.*?(?:CONCAT|[\+\|\|]).*?',
            content, re.IGNORECASE
        ):
            metadata["dynamic_sql"].append({
                "snippet": match.group(0)[:100],
                "line": content[:match.start()].count("\n") + 1,
            })

        # Detect dangerous operations (DROP, TRUNCATE, xp_cmdshell)
        for match in re.finditer(
            r'\b(DROP\s+TABLE|TRUNCATE\s+TABLE|xp_cmdshell|LOAD_FILE|INTO\s+OUTFILE|INTO\s+DUMPFILE)\b',
            content, re.IGNORECASE
        ):
            metadata["dangerous_operations"].append({
                "operation": match.group(1),
                "line": content[:match.start()].count("\n") + 1,
            })

        # Extract comments
        # Single-line comments
        for match in re.finditer(r'--\s*(.*?)$', content, re.MULTILINE):
            comment = match.group(1).strip()
            if comment:
                metadata["comments"].append({
                    "content": comment,
                    "line": content[:match.start()].count("\n") + 1,
                })
        # Block comments
        for match in re.finditer(r'/\*(.*?)\*/', content, re.DOTALL):
            comment = match.group(1).strip()
            if comment:
                metadata["comments"].append({
                    "content": comment,
                    "line": content[:match.start()].count("\n") + 1,
                })

        parsed.metadata = metadata
        return parsed

    def get_supported_extensions(self) -> list:
        return [".sql"]
