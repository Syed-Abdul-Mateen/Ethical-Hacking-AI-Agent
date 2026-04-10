"""
Detector for default credentials in code.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DefaultCredentialsDetector(BaseDetector):
    """Detects hardcoded default credentials."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        default_creds = [
            ("admin", "admin"),
            ("admin", "password"),
            ("root", "root"),
            ("root", "toor"),
            ("test", "test"),
            ("guest", "guest"),
            ("user", "user"),
        ]
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            for user, pwd in default_creds:
                # Look for patterns like username="admin", password="admin"
                # This is simplified
                pattern = re.compile(rf'username\s*=\s*["\']?{user}["\']?.*password\s*=\s*["\']?{pwd}["\']?', re.IGNORECASE)
                match = pattern.search(content)
                if match:
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="Default Credentials",
                        description=f"Default credentials '{user}/{pwd}' found.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="high",
                        cvss_score=8.0,
                        remediation="Change default credentials and enforce strong passwords. Do not hardcode credentials.",
                        cwe_id="CWE-798",
                    )
                    findings.append(finding)

        return findings