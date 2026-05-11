"""Generate reports from scan context."""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from src.orchestrator.context import ScanContext
from src.utils.logger import get_logger
from src.utils.config import Config
from src.reporting.exporters.pdf_exporter import PDFExporter

logger = get_logger(__name__)


class ReportGenerator:
    """Generate reports in various formats (HTML, JSON, Markdown, PDF, SARIF)."""

    def __init__(self, config: Config):
        self.config = config
        self.output_dir = config.get("reporting.output_dir", "./reports")
        self.formats = config.get("reporting.formats", ["html", "json"])
        self.templates_dir = config.get("reporting.templates_dir", "./src/reporting/templates")
        self.include_evidence = config.get("reporting.include_evidence", True)

        # Setup Exporters
        self.pdf_exporter = PDFExporter()
        
        # Setup Jinja2
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )

    def generate(self, context: ScanContext) -> Dict[str, Path]:
        """Generate all report formats and return paths."""
        report_paths = {}

        # Determine base output directory (use context.output_dir if set, else default)
        base_dir = context.output_dir or Path(self.output_dir)
        base_dir.mkdir(parents=True, exist_ok=True)

        # Create a scan-specific subdirectory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scan_dir = base_dir / f"scan_{timestamp}"
        scan_dir.mkdir(parents=True, exist_ok=True)

        # Prepare report data
        report_data = self._prepare_data(context)

        # Generate each format
        for fmt in self.formats:
            try:
                if fmt == "html":
                    path = self._generate_html(scan_dir, report_data)
                    if path:
                        report_paths["html"] = path
                elif fmt == "json":
                    path = self._generate_json(scan_dir, report_data)
                    if path:
                        report_paths["json"] = path
                elif fmt == "markdown":
                    path = self._generate_markdown(scan_dir, report_data)
                    if path:
                        report_paths["markdown"] = path
                elif fmt == "pdf":
                    path = self._generate_pdf(scan_dir, context)
                    if path:
                        report_paths["pdf"] = path
                elif fmt == "sarif":
                    path = self._generate_sarif(scan_dir, context)
                    if path:
                        report_paths["sarif"] = path
            except Exception as e:
                logger.error(f"Failed to generate {fmt} report: {e}", exc_info=True)

        # Always generate SARIF for CI/CD even if not explicitly in formats
        if "sarif" not in report_paths:
            try:
                path = self._generate_sarif(scan_dir, context)
                if path:
                    report_paths["sarif"] = path
            except Exception as e:
                logger.warning(f"SARIF generation failed: {e}")

        # Copy evidence if any and requested
        if self.include_evidence and context.temp_dir and context.temp_dir.exists():
            try:
                evidence_dir = scan_dir / "evidence"
                shutil.copytree(context.temp_dir, evidence_dir, dirs_exist_ok=True)
            except Exception as e:
                logger.warning(f"Failed to copy evidence: {e}")

        return report_paths

    def _generate_pdf(self, scan_dir: Path, context: ScanContext) -> Optional[Path]:
        """Generate PDF report."""
        try:
            output_path = scan_dir / "report.pdf"
            return self.pdf_exporter.export(context, output_path)
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return None

    def _prepare_data(self, context: ScanContext) -> Dict[str, Any]:
        """Convert scan context to serializable dict for templates."""
        findings_by_severity = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": [],
        }
        for finding in context.findings:
            severity = finding.severity
            if severity in findings_by_severity:
                findings_by_severity[severity].append(finding.to_dict())
            else:
                findings_by_severity["info"].append(finding.to_dict())

        return {
            "target": str(context.target_path),
            "scan_time": datetime.now().isoformat(),
            "files_scanned": len(context.files_scanned),
            "files_parsed": len(context.parsed_data),
            "total_findings": len(context.findings),
            "findings_by_severity": findings_by_severity,
            "findings": [f.to_dict() for f in context.findings],
            "vulnerable_dependencies": [
                dep.to_dict() if hasattr(dep, 'to_dict') else dep
                for dep in context.vulnerable_dependencies
            ],
            "secrets_findings": [
                s.to_dict() if hasattr(s, 'to_dict') else s
                for s in context.secrets_findings
            ],
            "dynamic_findings": [
                d.to_dict() if hasattr(d, 'to_dict') else d
                for d in context.dynamic_findings
            ],
            "errors": context.errors,
        }

    def _generate_html(self, scan_dir: Path, data: Dict[str, Any]) -> Optional[Path]:
        """Generate HTML report using template."""
        try:
            template = self.jinja_env.get_template("detailed_report.html")
            html_content = template.render(data=data)
            output_path = scan_dir / "report.html"
            output_path.write_text(html_content, encoding="utf-8")
            return output_path
        except Exception as e:
            logger.error(f"HTML report generation failed: {e}")
            return None

    def _generate_json(self, scan_dir: Path, data: Dict[str, Any]) -> Optional[Path]:
        """Generate JSON report."""
        output_path = scan_dir / "report.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return output_path

    def _generate_markdown(self, scan_dir: Path, data: Dict[str, Any]) -> Optional[Path]:
        """Generate Markdown report."""
        output_path = scan_dir / "report.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Security Scan Report\n\n")
            f.write(f"**Target:** {data['target']}\n\n")
            f.write(f"**Scan Date:** {data['scan_time']}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- Files Scanned: {data['files_scanned']}\n")
            f.write(f"- Files Parsed: {data['files_parsed']}\n")
            f.write(f"- Total Findings: {data['total_findings']}\n\n")
            f.write(f"### Findings by Severity\n\n")
            for sev, finds in data['findings_by_severity'].items():
                if finds:
                    f.write(f"- **{sev.capitalize()}**: {len(finds)}\n")
            f.write(f"\n## Detailed Findings\n\n")
            for finding in data['findings']:
                f.write(f"### {finding['title']}\n\n")
                f.write(f"- **Severity:** {finding['severity']}\n")
                f.write(f"- **File:** {finding['file_path']}\n")
                if finding.get('line_start'):
                    f.write(f"- **Line:** {finding['line_start']}\n")
                f.write(f"- **Description:** {finding['description']}\n")
                if finding.get('remediation'):
                    f.write(f"- **Remediation:** {finding['remediation']}\n")
                if finding.get('cwe_id'):
                    f.write(f"- **CWE:** {finding['cwe_id']}\n")
                if finding.get('cvss_score'):
                    f.write(f"- **CVSS Score:** {finding['cvss_score']}\n")
                f.write(f"\n---\n\n")
        return output_path

    def _generate_sarif(self, scan_dir: Path, context: ScanContext) -> Optional[Path]:
        """Generate SARIF 2.1.0 report for CI/CD integration."""
        try:
            from src.reporting.exporters.sarif_exporter import SARIFExporter
            exporter = SARIFExporter()
            output_path = scan_dir / "report.sarif.json"
            exporter.export(context, output_path)
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate SARIF report: {e}")
            return None