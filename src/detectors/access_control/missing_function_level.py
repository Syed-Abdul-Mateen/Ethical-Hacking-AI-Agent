"""
Detector for missing function-level access control.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MissingFunctionLevelDetector(BaseDetector):
    """Detects admin functions exposed without authentication checks."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for admin functions or endpoints that might lack auth
            # Common admin route patterns
            admin_routes = [
                r'/admin',
                r'admin\.php',
                r'manage',
                r'config',
                r'settings',
            ]
            # Check if there is any authentication check in the file (like session check)
            auth_check_patterns = [
                r'if\s*\(.*\$_SESSION',
                r'if\s*\(.*auth',
                r'@PreAuthorize',
                r'requires_authentication',
            ]
            has_auth_check = any(re.search(pattern, content, re.IGNORECASE) for pattern in auth_check_patterns)

            for route in admin_routes:
                if re.search(route, content, re.IGNORECASE) and not has_auth_check:
                    line = content[: content.find(route)].count("\n") + 1
                    finding = Finding(
                        title="Missing Function-Level Access Control",
                        description=f"Admin endpoint '{route}' found without authentication check.",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="high",
                        cvss_score=7.5,
                        remediation="Implement proper authentication and authorization checks for all admin functions.",
                        cwe_id="CWE-306",
                    )
                    findings.append(finding)

        return findings