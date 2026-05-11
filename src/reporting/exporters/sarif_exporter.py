"""SARIF 2.1.0 exporter for CI/CD integration (GitHub, Azure DevOps, etc.)."""

import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from src.orchestrator.context import ScanContext
from src.detectors.base_detector import Finding
from src.utils.logger import get_logger

logger = get_logger(__name__)

# SARIF 2.1.0 schema version
SARIF_VERSION = "2.1.0"
SARIF_SCHEMA = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"


class SARIFExporter:
    """
    Export scan findings in SARIF 2.1.0 format for integration with:
    - GitHub Code Scanning
    - Azure DevOps
    - SonarQube
    - Any SARIF-compatible CI/CD tool
    """

    SEVERITY_MAP = {
        "critical": "error",
        "high": "error",
        "medium": "warning",
        "low": "note",
        "info": "note",
    }

    SEVERITY_LEVEL_MAP = {
        "critical": "error",
        "high": "error",
        "medium": "warning",
        "low": "note",
        "info": "none",
    }

    def export(self, context: ScanContext, output_path: Path) -> Path:
        """
        Export scan results to SARIF format.

        Args:
            context: Completed scan context with findings.
            output_path: Path to write the SARIF JSON file.

        Returns:
            Path to the generated SARIF file.
        """
        sarif_document = self._build_sarif(context)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sarif_document, f, indent=2, default=str)

        logger.info(f"SARIF report generated: {output_path}")
        return output_path

    def _build_sarif(self, context: ScanContext) -> Dict[str, Any]:
        """Build the complete SARIF document."""
        rules = self._build_rules(context.findings)
        results = self._build_results(context.findings, context.target_path)

        return {
            "$schema": SARIF_SCHEMA,
            "version": SARIF_VERSION,
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "Ethical Hacking AI Agent",
                            "version": "0.1.0",
                            "semanticVersion": "0.1.0",
                            "informationUri": "https://github.com/yourusername/ethical_hacking_ai_agent",
                            "rules": rules,
                        }
                    },
                    "results": results,
                    "invocations": [
                        {
                            "executionSuccessful": True,
                            "startTimeUtc": datetime.now(timezone.utc).isoformat(),
                        }
                    ],
                    "columnKind": "utf16CodeUnits",
                }
            ],
        }

    def _build_rules(self, findings: List[Finding]) -> List[Dict[str, Any]]:
        """Build SARIF rule descriptors from unique finding types."""
        seen_rules = {}
        rules = []

        for finding in findings:
            rule_id = self._get_rule_id(finding)
            if rule_id not in seen_rules:
                rule = {
                    "id": rule_id,
                    "name": finding.title.replace(" ", ""),
                    "shortDescription": {
                        "text": finding.title,
                    },
                    "fullDescription": {
                        "text": finding.description,
                    },
                    "helpUri": f"https://cwe.mitre.org/data/definitions/{finding.cwe_id.split('-')[1]}.html"
                    if finding.cwe_id and '-' in finding.cwe_id else None,
                    "defaultConfiguration": {
                        "level": self.SEVERITY_LEVEL_MAP.get(finding.severity, "warning"),
                    },
                    "properties": {
                        "tags": [finding.cwe_id] if finding.cwe_id else [],
                        "security-severity": str(finding.cvss_score or 5.0),
                    },
                }
                # Remove None values
                rule = {k: v for k, v in rule.items() if v is not None}
                rules.append(rule)
                seen_rules[rule_id] = True

        return rules

    def _build_results(self, findings: List[Finding], target_path: Path) -> List[Dict[str, Any]]:
        """Build SARIF result entries from findings."""
        results = []

        for finding in findings:
            rule_id = self._get_rule_id(finding)

            result = {
                "ruleId": rule_id,
                "level": self.SEVERITY_MAP.get(finding.severity, "warning"),
                "message": {
                    "text": finding.description,
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": self._relative_uri(finding.file_path, target_path),
                                "uriBaseId": "%SRCROOT%",
                            },
                            "region": self._build_region(finding),
                        }
                    }
                ],
            }

            # Add fix information if remediation is available
            if finding.remediation:
                result["fixes"] = [
                    {
                        "description": {
                            "text": finding.remediation,
                        }
                    }
                ]

            # Add code snippet if available
            if finding.code_snippet:
                result["locations"][0]["physicalLocation"]["contextRegion"] = {
                    "snippet": {
                        "text": finding.code_snippet,
                    }
                }

            # Add fingerprint for deduplication
            result["fingerprints"] = {
                "primaryLocationLineHash": self._compute_fingerprint(finding),
            }

            results.append(result)

        return results

    @staticmethod
    def _get_rule_id(finding: Finding) -> str:
        """Generate a stable rule ID from the finding."""
        if finding.cwe_id:
            return finding.cwe_id
        return finding.title.replace(" ", "-").lower()

    @staticmethod
    def _relative_uri(file_path: Path, target_path: Path) -> str:
        """Convert absolute path to relative URI."""
        try:
            return str(Path(file_path).relative_to(target_path)).replace("\\", "/")
        except (ValueError, TypeError):
            return str(file_path).replace("\\", "/")

    @staticmethod
    def _build_region(finding: Finding) -> Dict[str, Any]:
        """Build SARIF region from finding line numbers."""
        region = {}
        if finding.line_start:
            region["startLine"] = finding.line_start
        if finding.line_end:
            region["endLine"] = finding.line_end
        if not region:
            region["startLine"] = 1
        return region

    @staticmethod
    def _compute_fingerprint(finding: Finding) -> str:
        """Compute a stable fingerprint for the finding."""
        import hashlib
        components = [
            str(finding.file_path),
            str(finding.line_start or 0),
            finding.title,
            finding.cwe_id or "",
        ]
        content = "|".join(components)
        return hashlib.sha256(content.encode()).hexdigest()[:32]
