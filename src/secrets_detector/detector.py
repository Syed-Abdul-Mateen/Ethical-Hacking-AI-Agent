"""
Main secrets detector.
"""

import re
import yaml
from typing import List, Dict, Any
from pathlib import Path

from src.detectors.base_detector import Finding
from src.utils.logger import get_logger

logger = get_logger(__name__)


class SecretsDetector:
    """Detects hardcoded secrets using regex patterns."""

    def __init__(self, patterns_file: str = None):
        self.patterns = self._load_patterns(patterns_file)

    def _load_patterns(self, patterns_file: str = None) -> List[Dict[str, Any]]:
        if patterns_file is None:
            patterns_file = Path(__file__).parent / "patterns.yaml"
        try:
            with open(patterns_file, "r") as f:
                data = yaml.safe_load(f)
            return data.get("patterns", [])
        except FileNotFoundError:
            logger.warning(f"Secrets patterns file not found: {patterns_file}")
            return []
        except Exception as e:
            logger.error(f"Error loading secrets patterns: {e}")
            return []

    def scan(self, content: str, file_path: str) -> List[Finding]:
        """Scan content for secrets."""
        findings = []
        for pattern in self.patterns:
            regex = pattern["regex"]
            name = pattern["name"]
            severity = pattern.get("severity", "high")
            remediation = pattern.get(
                "remediation",
                "Do not hardcode secrets. Use environment variables or secure vaults."
            )
            cwe_id = pattern.get("cwe", "CWE-798")
            try:
                compiled = re.compile(regex, re.IGNORECASE)
                for match in compiled.finditer(content):
                    line = content[: match.start()].count("\n") + 1
                    # Mask the secret for safe reporting
                    matched_text = match.group(0)
                    masked = matched_text[:10] + "..." if len(matched_text) > 14 else "***"
                    finding = Finding(
                        title=f"Hardcoded {name}",
                        description=f"Found {name} secret: {masked}",
                        file_path=file_path,
                        line_start=line,
                        severity=severity,
                        cvss_score=7.5,
                        remediation=remediation,
                        cwe_id=cwe_id,
                    )
                    findings.append(finding)
            except re.error as e:
                logger.warning(f"Invalid regex pattern for {name}: {e}")
        return findings