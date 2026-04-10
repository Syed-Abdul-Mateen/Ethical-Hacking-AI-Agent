"""
Update local vulnerability database from NVD.
"""

import json
import requests
from pathlib import Path
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)


class VulnDBUpdater:
    """Fetch latest CVE data from NVD API and update local cache."""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / "local_vuln_db.json"
        self.db_path = Path(db_path)

    def update(self):
        """Fetch latest vulnerabilities and save to file."""
        # For simplicity, we'll fetch a subset (e.g., recent CVEs)
        # In production, you'd want to use NVD API with pagination and caching.
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=100"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            # Transform to our format
            vulnerabilities = []
            for item in data.get("vulnerabilities", []):
                cve = item["cve"]
                descriptions = cve["descriptions"]
                desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "")
                # Extract package info from description? This is simplistic.
                # For demo, we'll just store the CVE ID and description.
                # Real implementation would need to parse affected products/versions.
                vuln = {
                    "id": cve["id"],
                    "description": desc,
                    "severity": "medium",  # Default
                    "cvss": 5.0,
                    "remediation": "Update to latest version.",
                    "cwe": "CWE-1035",
                }
                # If CVSS v3 is available
                if "metrics" in cve and "cvssMetricV31" in cve["metrics"]:
                    vuln["cvss"] = cve["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                    vuln["severity"] = cve["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"].lower()
                vulnerabilities.append(vuln)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.db_path, "w") as f:
                json.dump({"vulnerabilities": vulnerabilities}, f, indent=2)
            logger.info(f"Updated vulnerability database with {len(vulnerabilities)} entries.")
        except Exception as e:
            logger.error(f"Failed to update vulnerability database: {e}")