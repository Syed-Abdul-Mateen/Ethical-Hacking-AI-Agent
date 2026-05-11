from pathlib import Path
"""
Detector for missing rate limiting.
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimitingDetector(BaseDetector):
    """Detects missing rate limiting in API endpoints."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["php", "python", "java", "csharp", "ruby", "javascript"]:
                continue

            content = parsed_file.content
            # Look for rate limiting patterns
            rate_limiting_patterns = [
                r'rate_limit',
                r'throttle',
                r'limit_req',
                r'limiter',
                r'ratelimit',
            ]
            # If no rate limiting code is found and there are API endpoints, flag it
            # We'll detect endpoints by common patterns
            endpoint_patterns = [
                r'@app\.route',
                r'@RequestMapping',
                r'router\.(get|post)',
                r'\.get\(.*\)',
                r'\.post\(.*\)',
            ]
            has_endpoint = any(re.search(p, content, re.IGNORECASE) for p in endpoint_patterns)
            has_rate_limit = any(re.search(p, content, re.IGNORECASE) for p in rate_limiting_patterns)
            if has_endpoint and not has_rate_limit:
                finding = Finding(
                    title="Missing Rate Limiting",
                    description="API endpoints found but no rate limiting mechanisms detected.",
                    file_path=parsed_file.path,
                    line_start=None,
                    severity="medium",
                    cvss_score=5.0,
                    remediation="Implement rate limiting to prevent brute force attacks and DoS.",
                    cwe_id="CWE-770",
                )
                findings.append(finding)

        return findings
