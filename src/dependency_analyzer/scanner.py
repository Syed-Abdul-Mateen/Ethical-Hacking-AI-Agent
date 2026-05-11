"""
Main dependency scanner.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.dependency_analyzer.package_parsers import (
    NPMParser, PipParser, ComposerParser, GemParser, MavenParser
)
from src.detectors.base_detector import Finding
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DependencyScanner:
    """Scans package files for known vulnerabilities."""

    PARSERS = {
        "package.json": NPMParser,
        "package-lock.json": NPMParser,
        "requirements.txt": PipParser,
        "Pipfile.lock": PipParser,
        "composer.json": ComposerParser,
        "composer.lock": ComposerParser,
        "Gemfile.lock": GemParser,
        "pom.xml": MavenParser,
    }

    def __init__(self, vuln_db_path: str = None):
        if vuln_db_path is None:
            vuln_db_path = Path(__file__).parent / "local_vuln_db.json"
        self.vuln_db_path = vuln_db_path
        self.vuln_db = self._load_vuln_db()

    def _load_vuln_db(self) -> Dict[str, Any]:
        """Load local vulnerability database."""
        try:
            with open(self.vuln_db_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Vulnerability database not found. Run updater first.")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Malformed vulnerability database: {e}")
            return {}

    def scan_directory(self, root_path: Path) -> List[Finding]:
        """Scan a directory for package files and check dependencies."""
        findings = []
        for file_name, parser_cls in self.PARSERS.items():
            file_path = root_path / file_name
            if file_path.exists():
                try:
                    parser = parser_cls()
                    deps = parser.parse(file_path)
                    for dep in deps:
                        vuln = self._check_vulnerability(dep["name"], dep["version"])
                        if vuln:
                            finding = Finding(
                                title=f"Vulnerable Dependency: {dep['name']} {dep['version']}",
                                description=vuln["description"],
                                file_path=file_path,
                                line_start=None,
                                severity=vuln.get("severity", "medium"),
                                cvss_score=vuln.get("cvss", 5.0),
                                remediation=vuln.get("remediation", "Update to a patched version."),
                                cwe_id=vuln.get("cwe", "CWE-1035"),
                            )
                            findings.append(finding)
                except Exception as e:
                    logger.error(f"Error scanning {file_path}: {e}")
        return findings

    def _check_vulnerability(self, name: str, version: str) -> Optional[Dict[str, Any]]:
        """Check if a dependency version has known vulnerabilities."""
        for vuln in self.vuln_db.get("vulnerabilities", []):
            if vuln.get("package") == name:
                if "version" in vuln and version == vuln["version"]:
                    return vuln
        return None