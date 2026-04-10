"""
Detector for session fixation vulnerabilities.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SessionFixationDetector(BaseDetector):
    """Detects missing secure flags in cookies and session ID in URLs."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for cookie creation without HttpOnly or Secure flags
            # Also check for session ID in URL
            if parsed_file.language in ["php", "python", "java", "csharp", "ruby"]:
                # Check for setcookie without flags
                pattern = r'setcookie\s*\([^,]+,\s*[^,]+\)\s*;'  # only two args
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="Insecure Cookie",
                        description="Cookie set without HttpOnly or Secure flags.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="medium",
                        cvss_score=5.0,
                        remediation="Set HttpOnly and Secure flags on session cookies. Also set SameSite if appropriate.",
                        cwe_id="CWE-614",
                    )
                    findings.append(finding)

                # Check for session ID in URL
                pattern = r'[?&]session(id)?='
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="Session ID in URL",
                        description="Session identifier found in URL query string.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="medium",
                        cvss_score=5.5,
                        remediation="Do not pass session IDs in URLs. Use cookies with appropriate flags.",
                        cwe_id="CWE-598",
                    )
                    findings.append(finding)

        return findings