from pathlib import Path
"""
Detector for unsafe file uploads.
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class UnsafeFileUploadDetector(BaseDetector):
    """Detects file uploads without proper validation."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["php", "python", "java", "csharp", "ruby", "javascript"]:
                continue

            content = parsed_file.content
            # Look for file upload handling without validation
            upload_patterns = [
                r'move_uploaded_file',
                r'upload\.save',
                r'request\.FILES',
                r'@RequestPart',
                r'form\.parse',
            ]
            validation_patterns = [
                r'file\.type',
                r'mime_type',
                r'extension',
                r'validate',
            ]

            for upload_pattern in upload_patterns:
                if re.search(upload_pattern, content, re.IGNORECASE):
                    # Check if validation is present nearby (simplified)
                    has_validation = any(re.search(val, content, re.IGNORECASE) for val in validation_patterns)
                    if not has_validation:
                        finding = Finding(
                            title="Unsafe File Upload",
                            description="File upload detected without validation of file type or content.",
                            file_path=parsed_file.path,
                            line_start=None,
                            severity="medium",
                            cvss_score=6.5,
                            remediation="Validate file type, size, and content. Use a whitelist of allowed extensions and ensure files are stored outside web root.",
                            cwe_id="CWE-434",
                        )
                        findings.append(finding)

        return findings
