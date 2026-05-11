from pathlib import Path
"""
Detector for OS command injection vulnerabilities.
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CommandInjectionDetector(BaseDetector):
    """Detects OS command injection patterns."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        """Find command injection vulnerabilities in parsed files."""
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in self.config.get("languages", ["php", "python", "java", "csharp", "ruby", "go"]):
                continue

            dangerous_calls = getattr(parsed_file, "metadata", {}).get("dangerous_calls", [])
            for call in dangerous_calls:
                # Check if the argument contains user input
                # This is simplified; a real detector would need data flow analysis
                if self._is_user_input_in_call(parsed_file, call):
                    finding = Finding(
                        title="Command Injection",
                        description=f"Potential command injection via {call.get('name')}",
                        file_path=parsed_file.path,
                        line_start=call.get("line"),
                        severity="high",
                        cvss_score=9.0,
                        remediation="Avoid executing system commands with user input. Use safe APIs or escape arguments properly.",
                        cwe_id="CWE-78",
                    )
                    findings.append(finding)

        return findings

    def _is_user_input_in_call(self, parsed_file, call) -> bool:
        """Heuristic: check if the call contains variables that might be user-controlled."""
        # This would require data flow analysis; we'll use a simple pattern for now.
        # For demo, we just return True if the call exists.
        return True
