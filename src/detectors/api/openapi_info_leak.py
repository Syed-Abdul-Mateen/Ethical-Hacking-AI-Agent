from pathlib import Path
"""
Detector for exposed Swagger/OpenAPI documentation.
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OpenAPIInfoLeakDetector(BaseDetector):
    """Detects exposed OpenAPI/Swagger docs."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for swagger/openapi endpoints
            patterns = [
                r'swagger\.json',
                r'swagger\.yaml',
                r'openapi\.json',
                r'openapi\.yaml',
                r'/swagger/',
                r'/api-docs',
            ]
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    line = content[: content.find(pattern)].count("\n") + 1
                    finding = Finding(
                        title="Exposed API Documentation",
                        description=f"API documentation endpoint '{pattern}' found. This may expose internal API details.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="low",
                        cvss_score=2.5,
                        remediation="Restrict access to API documentation in production, or remove it entirely.",
                        cwe_id="CWE-200",
                    )
                    findings.append(finding)

        return findings
