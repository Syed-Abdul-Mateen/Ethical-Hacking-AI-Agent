"""
Detector for hardcoded weak passwords.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WeakPasswordsDetector(BaseDetector):
    """Detects hardcoded weak passwords."""

    WEAK_PASSWORDS = [
        "admin", "password", "123456", "qwerty", "letmein", "root", "toor", "test", "guest",
    "12345678", "12345", "123456789", "1234567890", "111111", "000000", "123123", "654321",
    "123321", "112233", "121212", "1234567", "password1", "passw0rd", "admin123", "root123",
    "welcome", "welcome1", "welcome123", "login", "secret", "secret123", "monkey", "dragon",
    "master", "master123", "sunshine", "shadow", "superman", "batman", "starwars", "michael",
    "jennifer", "jordan", "hunter", "freedom", "football", "baseball", "soccer", "hockey",
    "basketball", "chelsea", "arsenal", "liverpool", "microsoft", "google", "amazon", "facebook",
    "twitter", "linkedin", "qwerty123", "1qaz2wsx", "qazwsx", "zxcvbn", "asdfgh", "qwertyuiop",
    "iloveyou", "iloveyou1", "love", "loveme", "princess", "princess1", "solo", "solo123",
    "adminadmin", "passwordpassword", "changeme", "default", "pass123", "abc123", "abcd1234",
    "hello", "hello123", "whatever", "trustno1", "letmein123", "admin1", "root1", "test123",
    "guest123", "user", "user123", "ubuntu", "raspberry", "oracle", "cisco", "cisco123", "router",
    "switch", "firewall", "adminadmin123", "password123", "welcome2023", "admin2023", "pass@123"
    ]

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            for weak in self.WEAK_PASSWORDS:
                pattern = re.compile(rf'password\s*=\s*["\']({weak})["\']', re.IGNORECASE)
                for match in pattern.finditer(content):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="Hardcoded Weak Password",
                        description=f"Hardcoded weak password '{match.group(1)}' found.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="medium",
                        cvss_score=5.0,
                        remediation="Do not hardcode passwords. Use environment variables or secure configuration management.",
                        cwe_id="CWE-259",
                    )
                    findings.append(finding)

        return findings