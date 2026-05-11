"""
High entropy string detection.
"""

import math
from typing import List
import re

from src.detectors.base_detector import Finding
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HighEntropyDetector:
    """Detects strings with high Shannon entropy, which may indicate secrets."""

    def __init__(self, min_length: int = 16, entropy_threshold: float = 4.5):
        self.min_length = min_length
        self.entropy_threshold = entropy_threshold

    def shannon_entropy(self, s: str) -> float:
        """Calculate Shannon entropy of a string."""
        if not s:
            return 0.0
        freq = {}
        for c in s:
            freq[c] = freq.get(c, 0) + 1
        entropy = 0.0
        for count in freq.values():
            prob = count / len(s)
            entropy -= prob * math.log2(prob)
        return entropy

    def scan(self, content: str, file_path: str) -> List[Finding]:
        """Find high-entropy strings that might be secrets."""
        findings = []
        # Extract strings from code (simplified: any quoted strings)
        string_pattern = re.compile(r'["\']([^"\']{16,})["\']')
        for match in string_pattern.finditer(content):
            s = match.group(1)
            # Filter out common non-secret strings (like URLs, file paths)
            if s.startswith(('http://', 'https://', '/', 'C:', './', '../')):
                continue
            # Skip strings that are all whitespace or common prose
            if s.isspace() or ' ' in s and len(s.split()) > 3:
                continue
            if len(s) >= self.min_length:
                entropy = self.shannon_entropy(s)
                if entropy > self.entropy_threshold:
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="High Entropy String",
                        description=f"High entropy string (entropy {entropy:.2f}) found. May be a secret.",
                        file_path=file_path,
                        line_start=line,
                        severity="medium",
                        cvss_score=5.0,
                        remediation=(
                            "If this is a secret, remove it from code and use environment variables "
                            "or a secrets manager. If it is a legitimate string, consider adding "
                            "it to an ignore list."
                        ),
                        cwe_id="CWE-798",
                    )
                    findings.append(finding)
        return findings