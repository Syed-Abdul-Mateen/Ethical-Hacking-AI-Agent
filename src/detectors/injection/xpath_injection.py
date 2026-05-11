"""Detect XPath injection vulnerabilities."""

import re
from pathlib import Path
from typing import List, Dict

from src.detectors.base_detector import BaseDetector, Finding
from src.parsers.base_parser import ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class XpathInjectionDetector(BaseDetector):
    """
    Detects XPath injection patterns where user input is concatenated
    directly into XPath queries without proper sanitization.
    """

    # Patterns indicating XPath query construction with concatenation
    XPATH_PATTERNS = [
        # String concatenation with xpath/XPath function calls
        (r'xpath\s*\(\s*["\'].*?\+\s*\w+', "XPath query with string concatenation"),
        (r'selectNodes\s*\(\s*["\'].*?\+\s*\w+', "selectNodes with concatenation"),
        (r'selectSingleNode\s*\(\s*["\'].*?\+\s*\w+', "selectSingleNode with concatenation"),
        (r'evaluate\s*\(\s*["\'].*?//.*?\+\s*\w+', "XPath evaluate with concatenation"),
        # f-string / interpolation with xpath
        (r'xpath\s*\(\s*f["\']', "XPath with f-string interpolation"),
        # Variable interpolation in XPath expressions
        (r'xpath\s*\(\s*["\'].*?\{.*?\}', "XPath with variable interpolation"),
        # PHP-style concatenation
        (r'xpath\s*\(\s*["\'].*?\.\s*\$', "XPath with PHP variable concatenation"),
        # Java / C# string format
        (r'String\.format\s*\(\s*["\'].*?//.*?%s', "XPath with String.format"),
    ]

    # Keywords that indicate XPath usage context
    XPATH_CONTEXT_KEYWORDS = [
        "xpath", "xquery", "selectnodes", "selectsinglenode",
        "xmldocument", "xpathdocument", "lxml.etree",
        "xml.xpath", "xmlreader",
    ]

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []

        for file_path, parsed in parsed_data.items():
            content = parsed.content
            if not content:
                continue

            for line_num, line in enumerate(parsed.lines, start=1):
                line_lower = line.lower()

                # Quick check: does this line mention XPath at all?
                if not any(kw in line_lower for kw in self.XPATH_CONTEXT_KEYWORDS):
                    continue

                for pattern, desc in self.XPATH_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        snippet = parsed.get_snippet(line_num, context_lines=2)
                        finding = Finding(
                            title="Potential XPath Injection",
                            description=(
                                f"An XPath query appears to be constructed using dynamic input: {desc}. "
                                f"If user-controlled data is included without sanitization, an attacker "
                                f"can manipulate the query to access unauthorized data or bypass authentication."
                            ),
                            severity="high",
                            file_path=file_path,
                            line_start=line_num,
                            code_snippet=snippet,
                            remediation=(
                                "Use parameterized XPath queries or XPath variables instead of string concatenation. "
                                "Validate and sanitize all user input before including it in XPath expressions. "
                                "Consider using a whitelist approach for allowed characters."
                            ),
                            cwe_id="CWE-643",
                        )
                        findings.append(finding)
                        break  # One finding per line is sufficient

        return findings
