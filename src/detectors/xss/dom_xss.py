"""
Detector for DOM-based XSS.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DomXssDetector(BaseDetector):
    """Detects DOM-based XSS vulnerabilities in JavaScript."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language != "javascript":
                continue

            content = parsed_file.content
            # Look for dangerous sinks with user-controlled sources
            sinks = ["document.write", "innerHTML", "outerHTML", "eval", "setTimeout", "setInterval"]
            sources = ["location.hash", "location.search", "document.referrer", "window.name"]

            for sink in sinks:
                for source in sources:
                    pattern = re.compile(rf"{sink}\s*\([^)]*{source}", re.IGNORECASE)
                    for match in pattern.finditer(content):
                        line = content[: match.start()].count("\n") + 1
                        finding = Finding(
                            title="DOM-based XSS",
                            description=f"Potential DOM-based XSS: {sink} with {source}",
                            file_path=parsed_file.path,
                            line_start=line,
                            severity="medium",
                            cvss_score=6.5,
                            remediation="Avoid using dangerous sinks with untrusted data. Use safe APIs like textContent or proper encoding.",
                            cwe_id="CWE-79",
                        )
                        findings.append(finding)

        return findings