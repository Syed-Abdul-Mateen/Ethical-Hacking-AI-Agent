"""
Detector for insecure authentication practices.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class InsecureAuthDetector(BaseDetector):
    """Detects basic auth over HTTP, default credentials."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Basic auth over HTTP
            if re.search(r'Authorization:\s*Basic\s+', content, re.IGNORECASE):
                # We'll need to check if it's over HTTPS; but we can't know from code. We'll flag as warning.
                finding = Finding(
                    title="Basic Authentication",
                    description="Basic authentication used. Ensure it is over HTTPS only.",
                    file_path=parsed_file.path,
                    line_start=None,
                    severity="medium",
                    cvss_score=5.0,
                    remediation="Use HTTPS with basic auth or switch to more secure authentication mechanisms.",
                    cwe_id="CWE-522",
                )
                findings.append(finding)

            # Default credentials
            default_creds = ["admin/admin", "admin/password", "root/root"]
            for cred in default_creds:
                if cred in content:
                    line = content[: content.find(cred)].count("\n") + 1
                    finding = Finding(
                        title="Default Credentials",
                        description=f"Default credentials '{cred}' found.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="high",
                        cvss_score=8.0,
                        remediation="Remove default credentials and enforce strong passwords.",
                        cwe_id="CWE-798",
                    )
                    findings.append(finding)

        return findings