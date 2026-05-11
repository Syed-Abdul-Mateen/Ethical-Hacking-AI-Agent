"""
PDF Exporter for professional security audit reports.
Generates executive-level PDF documents from scan findings.
"""

from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from src.orchestrator.context import ScanContext
from src.detectors.base_detector import Finding
from src.utils.logger import get_logger

logger = get_logger(__name__)

try:
    from fpdf import FPDF
except ImportError:
    logger.warning("fpdf2 not installed. PDF export will be unavailable. Run: pip install fpdf2")
    FPDF = None


class PDFExporter:
    """
    Generates professional PDF security reports.
    Includes Executive Summary, Detailed Findings, and Remediation advice.
    """

    def __init__(self):
        self.enabled = FPDF is not None

    def export(self, context: ScanContext, output_path: Path) -> Path:
        """Export scan results to a PDF document."""
        if not self.enabled:
            raise ImportError("fpdf2 is required for PDF export. Run: pip install fpdf2")

        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_fill_color(15, 17, 26) # Dark background
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_font("Helvetica", 'B', 24)
        pdf.set_text_color(0, 255, 204) # Accent color
        pdf.cell(0, 20, "SECURITY AUDIT REPORT", ln=True, align='C')
        
        pdf.set_font("Helvetica", '', 12)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(20)

        # Executive Summary
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "Executive Summary", ln=True)
        pdf.set_font("Helvetica", '', 12)
        pdf.multi_cell(0, 10, f"Target: {context.target_path}\nFiles Scanned: {context.files_scanned_count}\nFindings Found: {len(context.findings)}")
        pdf.ln(10)

        # Findings Table Header
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(100, 10, "Vulnerability", 1, 0, 'C', True)
        pdf.cell(40, 10, "Severity", 1, 0, 'C', True)
        pdf.cell(50, 10, "CWE", 1, 1, 'C', True)

        # Findings Rows
        pdf.set_font("Helvetica", '', 10)
        for finding in context.findings:
            pdf.cell(100, 10, str(finding.title)[:50], 1)
            
            # Severity coloring
            if finding.severity.lower() == 'critical':
                pdf.set_text_color(255, 0, 127)
            elif finding.severity.lower() == 'high':
                pdf.set_text_color(255, 77, 77)
            else:
                pdf.set_text_color(0, 0, 0)
                
            pdf.cell(40, 10, finding.severity.upper(), 1, 0, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.cell(50, 10, finding.cwe_id or "N/A", 1, 1, 'C')

        # Detailed Remediation
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "Detailed Remediation Advice", ln=True)
        pdf.ln(5)
        
        for finding in context.findings:
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, f"Finding: {finding.title}", ln=True)
            pdf.set_font("Helvetica", '', 10)
            
            detail_text = f"File: {finding.file_path}\n"
            if finding.line_start:
                detail_text += f"Line: {finding.line_start}\n"
            
            # Add technical metadata for dynamic findings
            if finding.metadata:
                if "method" in finding.metadata:
                    detail_text += f"Method: {finding.metadata['method'].upper()}\n"
                if "param" in finding.metadata:
                    detail_text += f"Parameter: {finding.metadata['param']}\n"
                if "payload" in finding.metadata:
                    detail_text += f"Payload: {finding.metadata['payload']}\n"
            
            detail_text += f"\nDescription: {finding.description}\n\nRemediation: {finding.remediation}\n"
            pdf.multi_cell(0, 7, detail_text)
            pdf.ln(5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

        pdf.output(str(output_path))
        logger.info(f"PDF report generated at: {output_path}")
        return output_path
