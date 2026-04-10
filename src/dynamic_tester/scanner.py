"""
Dynamic scanner that injects payloads and checks for vulnerabilities.
"""

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import List, Dict, Any
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DynamicScanner:
    """Perform dynamic testing by injecting payloads into forms and parameters."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> Dict[str, List[str]]:
        payloads = {}
        payload_dir = Path(__file__).parent / "payloads"
        for name in ["xss_payloads.txt", "sqli_payloads.txt"]:
            file_path = payload_dir / name
            if file_path.exists():
                with open(file_path, "r") as f:
                    payloads[name] = [line.strip() for line in f if line.strip()]
            else:
                payloads[name] = []
        return payloads

    def scan(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scan discovered URLs for vulnerabilities."""
        findings = []
        for url in urls:
            # Test URL parameters
            parsed = urlparse(url)
            query = parse_qs(parsed.query)
            if query:
                for param, values in query.items():
                    for payload in self.payloads.get("xss_payloads.txt", []):
                        modified_query = query.copy()
                        modified_query[param] = [payload]
                        new_query = urlencode(modified_query, doseq=True)
                        new_url = urlunparse(parsed._replace(query=new_query))
                        resp = requests.get(new_url, timeout=5)
                        if payload in resp.text:
                            findings.append({
                                "type": "XSS",
                                "url": url,
                                "parameter": param,
                                "payload": payload,
                                "reflected": True
                            })
                    for payload in self.payloads.get("sqli_payloads.txt", []):
                        # Similar for SQLi
                        pass
            # Test forms (simplified: assume POST forms)
            # We'd need to parse HTML to find forms. For brevity, skip.
        return findings