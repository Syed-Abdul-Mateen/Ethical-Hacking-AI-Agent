"""
Detector for weak encryption algorithms.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WeakEncryptionDetector(BaseDetector):
    """Detects use of weak cryptographic algorithms."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            weak_algorithms = ["md5", "sha1", "des", "rc4", "ecb"]
            for algo in weak_algorithms:
                pattern = re.compile(rf'\b{algo}\b', re.IGNORECASE)
                for match in pattern.finditer(content):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="Weak Encryption",
                        description=f"Use of weak or deprecated cryptographic algorithm: {match.group(0)}",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="medium",
                        cvss_score=5.0,
                        remediation="Use strong, modern algorithms like AES-256, SHA-256, and avoid ECB mode. Use secure key management.",
                        cwe_id="CWE-326",
                    )
                    findings.append(finding)

        return findings