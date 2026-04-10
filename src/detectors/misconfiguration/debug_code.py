"""
Detector for debug code left in production.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DebugCodeDetector(BaseDetector):
    """Detects debug endpoints and verbose error messages."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for debug functions or endpoints
            debug_patterns = [
                r'debug\s*\(',          # debug()
                r'console\.log',        # JavaScript console.log
                r'var_dump',            # PHP var_dump
                r'print_r',             # PHP print_r
                r'error_reporting\(E_ALL\)', # PHP error reporting
                r'@app\.route\(.*/debug', # Flask debug route
                r'if\s*\(.*debug',      # Conditionals with debug
                r'debug=True',          # Flask debug mode
                r'DEBUG\s*=\s*True',    # Django debug
            ]
            for pattern in debug_patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="Debug Code",
                        description=f"Debug code or verbose error reporting found: {match.group(0)}",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="low",
                        cvss_score=2.0,
                        remediation="Remove debug code and disable verbose error messages in production. Use proper logging instead.",
                        cwe_id="CWE-489",
                    )
                    findings.append(finding)

        return findings