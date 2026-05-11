from pathlib import Path
"""
Detector for GraphQL introspection enabled.
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GraphqlIntrospectionDetector(BaseDetector):
    """Detects GraphQL introspection enabled in production."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["javascript", "python", "java", "csharp"]:
                continue

            content = parsed_file.content
            # Look for GraphQL endpoint with introspection not disabled
            # Typically, introspection is enabled by default
            # We'll check if there's a pattern that disables it
            disabled_patterns = [
                r'introspection\s*:\s*false',
                r'\.disableIntrospection\(\)',
                r'GraphQL::disable_introspection',
            ]
            if re.search(r'graphql', content, re.IGNORECASE):
                if not any(re.search(p, content, re.IGNORECASE) for p in disabled_patterns):
                    finding = Finding(
                        title="GraphQL Introspection Enabled",
                        description="GraphQL introspection is likely enabled. This can leak schema information.",
                        file_path=parsed_file.path,
                        line_start=None,
                        severity="low",
                        cvss_score=3.0,
                        remediation="Disable GraphQL introspection in production environments to prevent schema leakage.",
                        cwe_id="CWE-200",
                    )
                    findings.append(finding)

        return findings
