"""
Detector for large memory allocations based on user input.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LargeAllocationsDetector(BaseDetector):
    """Detects loops that allocate large structures based on user input."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for loops that allocate memory based on a variable that might be user-controlled
            # Patterns: for i in range(user_input): list.append(...)
            pattern = r'for\s+.*\s+in\s+range\s*\(\s*\$_'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line = content[: match.start()].count("\n") + 1
                finding = Finding(
                    title="Potential Memory Exhaustion",
                    description=f"Loop that allocates memory based on user input: {match.group(0)}",
                    file_path=parsed_file.path,
                    line_start=line,
                    severity="medium",
                    cvss_score=5.0,
                    remediation="Set limits on user input that controls loop iterations or memory allocation.",
                    cwe_id="CWE-400",
                )
                findings.append(finding)

        return findings