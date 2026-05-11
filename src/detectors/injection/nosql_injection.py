from pathlib import Path
"""
Detector for NoSQL injection (MongoDB, etc.).
"""

import re
from src.parsers.base_parser import ParsedFile
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger

logger = get_logger(__name__)


class NoSQLInjectionDetector(BaseDetector):
    """Detects NoSQL injection patterns."""

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []
        for _, parsed_file in parsed_data.items():
            if parsed_file.language not in ["javascript", "python", "java"]:
                continue

            # Look for MongoDB queries with user input
            content = parsed_file.content
            # Patterns: db.collection.find({$where: ...}) or col.find({username: req.body.username})
            # Simplified: any query object that contains variable interpolation
            patterns = [
                (r'db\.\w+\.(find|findOne|update|insert|remove)\s*\(\s*{[^}]*\$\{', "MongoDB injection"),
                (r'\$where\s*:', "MongoDB $where injection"),
                (r'\.find\s*\(\s*{[^}]*\$\{', "User input in query"),
            ]
            for pattern, desc in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line = content[: match.start()].count("\n") + 1
                    finding = Finding(
                        title="NoSQL Injection",
                        description=f"Potential NoSQL injection: {desc}",
                        file_path=parsed_file.path,
                        line_start=line,
                        severity="high",
                        cvss_score=8.0,
                        remediation="Use parameterized queries or properly validate and sanitize user input before constructing NoSQL queries.",
                        cwe_id="CWE-943",
                    )
                    findings.append(finding)

        return findings
