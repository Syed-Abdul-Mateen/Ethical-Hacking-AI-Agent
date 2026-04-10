"""
Markdown report exporter.
"""

from pathlib import Path
from typing import List
from src.detectors.base_detector import Finding


class MarkdownExporter:
    """Export findings to Markdown."""

    def export(self, findings: List[Finding], output_path: Path, scan_summary: dict = None):
        """Generate Markdown report."""
        lines = []
        lines.append("# Security Scan Report")
        if scan_summary:
            lines.append("## Summary")
            for key, value in scan_summary.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        lines.append("## Findings")
        if not findings:
            lines.append("No findings.")
        else:
            for idx, finding in enumerate(findings, 1):
                lines.append(f"### {idx}. {finding.title}")
                lines.append(f"- **Severity**: {finding.severity}")
                lines.append(f"- **CVSS Score**: {finding.cvss_score}")
                lines.append(f"- **File**: {finding.file_path}")
                if finding.line_number:
                    lines.append(f"- **Line**: {finding.line_number}")
                lines.append(f"- **Description**: {finding.description}")
                lines.append(f"- **Remediation**: {finding.remediation}")
                if finding.cwe_id:
                    lines.append(f"- **CWE**: {finding.cwe_id}")
                lines.append("")
        output_path.write_text("\n".join(lines), encoding="utf-8")