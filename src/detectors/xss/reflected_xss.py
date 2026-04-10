"""Detect potential reflected XSS vulnerabilities."""

import re
from pathlib import Path
from typing import List, Dict

from src.detectors.base_detector import BaseDetector, Finding
from src.parsers.base_parser import ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReflectedXssDetector(BaseDetector):
    """
    Detects reflected XSS patterns:
    - Output of user input without proper encoding (e.g., echo $_GET['x'])
    - Direct rendering of request parameters in HTML
    """

    # Dangerous patterns: output of request data without escaping
    REFLECTED_PATTERNS = [
        r'echo\s*\$\_(GET|POST|REQUEST)\[',               # PHP: echo $_GET[...]
        r'print\s*\$\_(GET|POST|REQUEST)\[',
        r'\<\?=\s*\$\_(GET|POST|REQUEST)\[',               # PHP short echo tag
        r'response\.write\(.*?req\.(query|body)',         # Node.js
        r'innerHTML\s*=\s*.*?location\.search',           # JavaScript DOM XSS (reflected)
        r'document\.write\(.*?location\.search',
        r'\.html\(.*?req\.(param|query)',                 # Express-like
        r'<%=.*?req\.(query|param)',                      # EJS/ERB
    ]

    # Contexts where output should be encoded (simplistic)
    CONTEXT_HTML = re.compile(r'<[^>]*>')

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []

        for file_path, parsed in parsed_data.items():
            # Applicable to server-side languages (PHP, Python, Node, Java) and client-side JS
            if parsed.language not in ("php", "python", "javascript", "java", "csharp", "ruby", "html"):
                continue

            for line_num, line in enumerate(parsed.lines, start=1):
                # Check for patterns indicating reflection
                dangerous = False
                for pattern in self.REFLECTED_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        dangerous = True
                        break

                if dangerous:
                    snippet = parsed.get_snippet(line_num, context_lines=2)
                    finding = Finding(
                        title="Potential Reflected XSS",
                        description="User input appears to be directly output to the HTML response without proper encoding or sanitization. This can lead to reflected Cross-Site Scripting (XSS) if the input contains malicious scripts.",
                        severity="high",
                        file_path=file_path,
                        line_start=line_num,
                        code_snippet=snippet,
                        remediation="Always escape output based on the context (HTML, JavaScript, URL, etc.). Use a templating engine that auto-escapes, or manually apply functions like htmlspecialchars() in PHP, or equivalent in other languages.",
                        cwe_id="CWE-79",
                    )
                    findings.append(finding)

        return findings