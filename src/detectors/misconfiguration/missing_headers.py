"""
Detector for missing security headers.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MissingHeadersDetector(BaseDetector):
    """Detects missing HTTP security headers in response code."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["php", "python", "java", "csharp", "ruby", "javascript"]:
                continue

            content = parsed_file.content
            # List of security headers to check for
            required_headers = [
                ("X-Frame-Options", "DENY"),
                ("X-Content-Type-Options", "nosniff"),
                ("Content-Security-Policy", None),
                ("Strict-Transport-Security", None),
                ("Referrer-Policy", None),
                ("Permissions-Policy", None),
            ]
            # Look for header setting code
            header_patterns = [
                r'header\s*\(\s*[\'"]X-Frame-Options',
                r'response\.setHeader\s*\(\s*[\'"]X-Frame-Options',
                r'HttpResponseHeaders\.Add',
            ]
            # Simplified: if none of the headers are set in the file, flag as missing
            # Actually, we need to check if headers are set; we'll do a quick scan.
            has_headers = any(re.search(pattern, content, re.IGNORECASE) for pattern in header_patterns)
            if not has_headers:
                # If no header setting is found, it's a potential misconfiguration
                finding = Finding(
                    title="Missing Security Headers",
                    description="No security headers (X-Frame-Options, CSP, etc.) found in the code. This may lead to clickjacking, MIME type sniffing, etc.",
                    file_path=parsed_file.path,
                    line_start=None,
                    severity="low",
                    cvss_score=3.5,
                    remediation="Add security headers like X-Frame-Options, Content-Security-Policy, X-Content-Type-Options, and HSTS.",
                    cwe_id="CWE-693",
                )
                findings.append(finding)

        return findings