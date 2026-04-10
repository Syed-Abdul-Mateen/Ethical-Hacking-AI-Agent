"""
Detector for Insecure Direct Object Reference (IDOR) patterns.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class IDORDetector(BaseDetector):
    """Detects potential IDOR vulnerabilities."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["php", "python", "java", "csharp", "ruby", "javascript"]:
                continue

            content = parsed_file.content
            # Look for patterns where user input (like $_GET['id']) is used directly in database queries
            # without permission checks.
            user_input_patterns = [
                r'\$_GET\[[^\]]+\]',
                r'\$_POST\[[^\]]+\]',
                r'request\.GET',
                r'request\.POST',
                r'request\.args',
                r'@PathVariable',
                r'@RequestParam',
            ]
            db_patterns = [
                r'SELECT\s+.*\s+FROM\s+\w+\s+WHERE',
                r'db\.\w+\.find',
                r'\.query\(.*\?',
            ]

            for user_input in user_input_patterns:
                for db_pattern in db_patterns:
                    # Simplified: if user input appears near a db query
                    # We'll use a simple heuristic: any line that contains both patterns
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if re.search(user_input, line, re.IGNORECASE) and re.search(db_pattern, line, re.IGNORECASE):
                            finding = Finding(
                                title="Potential IDOR",
                                description=f"User input used in database query without apparent authorization check: {line.strip()}",
                                file_path=parsed_file.path,
                                line_start=i+1,
                                severity="medium",
                                cvss_score=5.5,
                                remediation="Ensure that users can only access objects they are authorized to. Implement proper access control checks.",
                                cwe_id="CWE-639",
                            )
                            findings.append(finding)

        return findings