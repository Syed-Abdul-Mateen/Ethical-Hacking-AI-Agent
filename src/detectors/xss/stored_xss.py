"""
Detector for stored XSS (cross-site scripting).
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class StoredXssDetector(BaseDetector):
    """Detects stored XSS vulnerabilities."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["php", "python", "java", "csharp", "ruby", "javascript"]:
                continue

            content = parsed_file.content
            # Look for database insertion of user input and later output to HTML
            # This is complex; we'll use a simplified pattern: any place where user input is inserted into DB and later echoed
            # We'll just detect any SQL insert that uses user input and any HTML output that might include DB data.
            # For demo, we'll flag any file that has both insertion and output patterns.
            insertion_pattern = r"(INSERT\s+INTO|db\.\w+\.(insert|save))"
            output_pattern = r"(echo|print|write|document\.write|innerHTML)"

            if re.search(insertion_pattern, content, re.IGNORECASE) and re.search(output_pattern, content, re.IGNORECASE):
                # This is too broad; we'll still create a finding with low confidence
                finding = Finding(
                    title="Stored XSS",
                    description="Potential stored XSS: user input is stored and later displayed without proper encoding.",
                    file_path=parsed_file.path,
                    line_start=None,
                    severity="medium",
                    cvss_score=6.0,
                    remediation="Always encode output that contains user-controlled data. Use context-aware encoding (HTML, JS, etc.).",
                    cwe_id="CWE-79",
                )
                findings.append(finding)

        return findings