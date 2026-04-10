"""
Detector for path traversal vulnerabilities.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PathTraversalDetector(BaseDetector):
    """Detects path traversal patterns."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for file operations with user input containing '..'
            user_input_patterns = [
                r'\$_GET\[[^\]]+\]',
                r'\$_POST\[[^\]]+\]',
                r'request\.GET',
                r'request\.POST',
            ]
            file_patterns = [
                r'file_get_contents',
                r'fopen',
                r'open\(',
                r'File\.ReadAllText',
                r'os\.Open',
                r'readfile',
                r'include',
                r'require',
            ]
            for user_input in user_input_patterns:
                for file_pattern in file_patterns:
                    # Look for line containing both patterns
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if re.search(user_input, line, re.IGNORECASE) and re.search(file_pattern, line, re.IGNORECASE):
                            # Check if the line contains '..'
                            if '..' in line:
                                finding = Finding(
                                    title="Path Traversal",
                                    description=f"Potential path traversal using user input: {line.strip()}",
                                    file_path=parsed_file.path,
                                    line_start=i+1,
                                    severity="high",
                                    cvss_score=7.5,
                                    remediation="Sanitize user input used in file paths. Use a whitelist of allowed files or normalize paths and check against a base directory.",
                                    cwe_id="CWE-22",
                                )
                                findings.append(finding)

        return findings