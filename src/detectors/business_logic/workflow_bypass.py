"""
Detector for workflow bypass vulnerabilities.
"""

import re
from typing import List

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowBypassDetector(BaseDetector):
    """Detects missing state checks in workflows."""

    def run(self, parsed_data: dict) -> list:
        findings = []
        for _, parsed_file in parsed_data.items():
            content = parsed_file.content
            # Look for workflows that might be bypassed by directly accessing endpoints
            # This is complex; we'll use a simple pattern: check if there are state variables but no verification
            # Example: a multi-step form where step is passed via GET parameter
            step_pattern = r'step\s*=\s*\$_GET'
            if re.search(step_pattern, content, re.IGNORECASE):
                # Check if there is a validation of the step order
                if not re.search(r'if\s*\(.*step.*\w+\)', content):
                    finding = Finding(
                        title="Workflow Bypass",
                        description="Potential workflow bypass: step parameter can be manipulated to skip steps.",
                        file_path=parsed_file.path,
                        line_start=None,
                        severity="medium",
                        cvss_score=6.0,
                        remediation="Validate that the user is at the correct step in the workflow. Use server-side state tracking.",
                        cwe_id="CWE-841",
                    )
                    findings.append(finding)

        return findings