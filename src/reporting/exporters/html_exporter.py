"""
HTML report exporter.
"""

import jinja2
from pathlib import Path
from typing import List
from src.detectors.base_detector import Finding


class HTMLExporter:
    """Export findings to HTML."""

    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates"
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_dir)))

    def export(self, findings: List[Finding], output_path: Path, scan_summary: dict = None):
        """Generate HTML report."""
        template = self.env.get_template("detailed_report.html")
        html = template.render(findings=findings, summary=scan_summary or {})
        output_path.write_text(html, encoding="utf-8")