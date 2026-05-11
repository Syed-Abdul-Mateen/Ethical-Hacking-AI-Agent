from pathlib import Path
"""
Detector for Local/Remote File Inclusion (LFI/RFI).
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class FileInclusionDetector(BaseDetector):
    """Detects LFI/RFI vulnerabilities."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language != "php":
                continue

            content = parsed_file.content
            # Look for include/require with user input
            patterns = [
                (r'include\s*\(\s*\$_', "Local File Inclusion"),
                (r'require\s*\(\s*\$_', "Local File Inclusion"),
                (r'include\s*\(\s*\$', "Local File Inclusion"),
                (r'require\s*\(\s*\$', "Local File Inclusion"),
            ]
            for pattern, desc in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="File Inclusion",
                        description=f"Potential {desc} using user-controlled input.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="high",
                        cvss_score=8.0,
                        remediation="Avoid including files based on user input. If necessary, use a whitelist of allowed files and sanitize input.",
                        cwe_id="CWE-98",
                    )
                    findings.append(finding)

        return findings
