"""
Detector for PHP unserialize.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PHPDeserializeDetector(BaseDetector):
    """Detects unsafe use of unserialize()."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language != "php":
                continue

            content = parsed_file.content
            # Look for unserialize with user input
            pattern = r'unserialize\s*\(\s*\$_'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line = content[: match.start()].count("\n") + 1
                finding = Finding(
                    title="Insecure Deserialization",
                    description="Unsafe use of unserialize() with user input. This can lead to remote code execution.",
                    file_path=parsed_file.path,
                    line_start=line,
                    severity="critical",
                    cvss_score=9.0,
                    remediation="Avoid unserializing untrusted data. Use JSON or other safe formats if possible. If necessary, use allow_classes with strict whitelist.",
                    cwe_id="CWE-502",
                )
                findings.append(finding)

        return findings