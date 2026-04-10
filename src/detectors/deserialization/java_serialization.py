"""
Detector for Java ObjectInputStream.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class JavaSerializationDetector(BaseDetector):
    """Detects unsafe use of ObjectInputStream."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language != "java":
                continue

            content = parsed_file.content
            pattern = r'new\s+ObjectInputStream\s*\('
            for match in re.finditer(pattern, content):
                line = content[: match.start()].count("\n") + 1
                finding = Finding(
                    title="Insecure Deserialization",
                    description="Unsafe use of ObjectInputStream. Deserializing untrusted data can lead to remote code execution.",
                    file_path=parsed_file.path,
                    line_start=line,
                    severity="critical",
                    cvss_score=9.0,
                    remediation="Avoid deserializing untrusted data. Use JSON or other safe formats. If necessary, use a whitelist of allowed classes with LookaheadObjectInputStream.",
                    cwe_id="CWE-502",
                )
                findings.append(finding)

        return findings