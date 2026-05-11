"""Parser for C# and ASP.NET files."""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CSharpParser(BaseParser):
    """
    Parser for C# and ASP.NET files.
    Extracts classes, methods, attributes, SQL queries, and security-relevant patterns.
    """

    def __init__(self, config):
        super().__init__(config)
        self.language = "csharp"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)

        metadata: Dict[str, Any] = {
            "namespaces": [],
            "classes": [],
            "methods": [],
            "attributes": [],
            "using_directives": [],
            "sql_queries": [],
            "http_handlers": [],
            "dangerous_calls": [],
        }

        # Extract using directives
        for match in re.finditer(r'using\s+([\w.]+)\s*;', content):
            metadata["using_directives"].append(match.group(1))

        # Extract namespace declarations
        for match in re.finditer(r'namespace\s+([\w.]+)', content):
            metadata["namespaces"].append(match.group(1))

        # Extract class definitions
        for match in re.finditer(
            r'(?:public|private|protected|internal|static|abstract|sealed|\s)*\s*class\s+(\w+)',
            content
        ):
            metadata["classes"].append(match.group(1))

        # Extract method definitions
        for match in re.finditer(
            r'(?:public|private|protected|internal|static|virtual|override|async|\s)*\s+'
            r'(?:[\w<>\[\],\s]+)\s+(\w+)\s*\(',
            content
        ):
            method_name = match.group(1)
            # Filter out common non-method keywords
            if method_name not in ("if", "while", "for", "switch", "catch", "class", "new", "return"):
                metadata["methods"].append(method_name)

        # Extract attributes (decorators) like [Authorize], [HttpPost], [AllowAnonymous]
        for match in re.finditer(r'\[(\w+)(?:\(.*?\))?\]', content):
            metadata["attributes"].append(match.group(1))

        # Extract SQL queries (string concat with SQL keywords)
        for match in re.finditer(
            r'(?:"[^"]*(?:SELECT|INSERT|UPDATE|DELETE|FROM|WHERE)[^"]*"\s*\+)',
            content, re.IGNORECASE
        ):
            metadata["sql_queries"].append({
                "snippet": match.group(0)[:100],
                "line": content[:match.start()].count("\n") + 1,
            })

        # Detect HttpContext / Request usage (user input sources in ASP.NET)
        for match in re.finditer(
            r'(?:Request|HttpContext)\.(?:QueryString|Form|Cookies|Headers|Params)\[',
            content
        ):
            metadata["http_handlers"].append({
                "access": match.group(0),
                "line": content[:match.start()].count("\n") + 1,
            })

        # Detect dangerous calls
        dangerous_patterns = [
            (r'Process\.Start\s*\(', "Process.Start"),
            (r'SqlCommand\s*\([^)]*\+', "SqlCommand with concatenation"),
            (r'\.ExecuteNonQuery\s*\(', "ExecuteNonQuery"),
            (r'\.ExecuteReader\s*\(', "ExecuteReader"),
            (r'Response\.Write\s*\(', "Response.Write"),
            (r'eval\s*\(', "eval"),
        ]
        for pattern, name in dangerous_patterns:
            for match in re.finditer(pattern, content):
                metadata["dangerous_calls"].append({
                    "call": name,
                    "line": content[:match.start()].count("\n") + 1,
                })

        parsed.metadata = metadata
        return parsed

    def get_supported_extensions(self) -> list:
        return [".cs", ".aspx", ".ashx", ".asmx"]
