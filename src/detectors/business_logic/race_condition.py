"""
Detector for race condition vulnerabilities.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RaceConditionDetector(BaseDetector):
    """Detects potential race conditions."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for non-atomic operations that might be vulnerable to race conditions
            # Examples: check-then-act patterns without locking
            # Simplified: find operations that read, then write, without synchronization
            # We'll look for patterns like if (balance >= amount) { balance -= amount; }
            pattern = r'if\s*\([^)]+\)\s*\{[^}]*\w+\s*[+-]=\s*\w+'
            matches = re.finditer(pattern, content)
            for match in matches:
                line = content[: match.start()].count("\n") + 1
                # Check if there is any locking mechanism around
                # This is a heuristic; we'll just flag as potential
                finding = Finding(
                    title="Potential Race Condition",
                    description="Non-atomic check-then-act operation detected. This could lead to race conditions.",
                    file_path=parsed_file.path,
                    line_start=line,
                    severity="medium",
                    cvss_score=5.0,
                    remediation="Use proper synchronization (locks, atomic operations, or transactions) to ensure thread safety.",
                    cwe_id="CWE-362",
                )
                findings.append(finding)

        return findings