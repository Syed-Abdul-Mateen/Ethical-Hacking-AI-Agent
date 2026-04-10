"""
Detector for LDAP injection.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LDAPInjectionDetector(BaseDetector):
    """Detects LDAP injection patterns."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["java", "php", "python", "csharp"]:
                continue

            content = parsed_file.content
            # Look for LDAP search filters with concatenation
            patterns = [
                (r'ldap\.search\s*\([^,]+,\s*"\([^"]*\+\s*\w+', "LDAP search filter concatenation"),
                (r'new\s+LdapContext\s*\([^,]+,\s*"\([^"]*\+\s*\w+', "LDAP context with concatenation"),
            ]
            for pattern, desc in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="LDAP Injection",
                        description=f"Potential LDAP injection: {desc}",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="high",
                        cvss_score=8.0,
                        remediation="Use LDAP search filters with parameterized queries or escape special characters.",
                        cwe_id="CWE-90",
                    )
                    findings.append(finding)

        return findings