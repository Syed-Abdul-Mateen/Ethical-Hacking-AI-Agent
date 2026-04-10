"""
Detector for ReDoS (Regular Expression Denial of Service).
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ReDoSDetector(BaseDetector):
    """Detects regex patterns vulnerable to catastrophic backtracking."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for regex patterns that might be vulnerable
            # Simplified: patterns with nested quantifiers like (a+)+
            pattern = re.compile(r'[^\\]\('[^)]*\+[^)]*\+', re.IGNORECASE)
            for match in pattern.finditer(content):
                # Extract the regex pattern if possible
                line = content[: match.start()].count("\n") + 1
                finding = Finding(
                    title="ReDoS Vulnerability",
                    description=f"Potential ReDoS: regex pattern with nested quantifiers: {match.group(0)}",
                    file_path=parsed_file.path,
                    line_start=line,
                    severity="medium",
                    cvss_score=5.0,
                    remediation="Avoid regex patterns with nested quantifiers. Use atomic grouping or possessive quantifiers if supported.",
                    cwe_id="CWE-1333",
                )
                findings.append(finding)

        return findings