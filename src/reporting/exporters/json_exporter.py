"""
JSON report exporter.
"""

import json
from pathlib import Path
from typing import List
from src.detectors.base_detector import Finding


class JSONExporter:
    """Export findings to JSON."""

    def export(self, findings: List[Finding], output_path: Path, scan_summary: dict = None):
        """Generate JSON report."""
        data = {
            "scan_summary": scan_summary or {},
            "findings": [finding.to_dict() for finding in findings]
        }
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)