"""
Dynamic scanner that injects payloads and checks for vulnerabilities.
Integrates with server_launcher and crawler for full dynamic testing workflow.
"""

import requests
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.detectors.base_detector import Finding
from src.dynamic_tester.server_launcher import ServerLauncher
from src.dynamic_tester.crawler import Crawler
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


class DynamicScanner:
    """
    Perform dynamic testing by:
    1. Launching a local server for the target project
    2. Crawling to discover URLs
    3. Injecting payloads into forms and parameters
    4. Analyzing responses for vulnerability indicators
    """

    def __init__(self, config: Config, context: Any):
        self.config = config
        self.context = context
        self.payloads = self._load_payloads()
        self.timeout = config.get("dynamic.scanner.timeout", 5)
        self.max_urls = config.get("dynamic.max_urls", 100)
        self.server_launcher: Optional[ServerLauncher] = None
        self.base_url: Optional[str] = None

    def _load_payloads(self) -> Dict[str, List[str]]:
        """Load attack payloads from files."""
        payloads = {}
        payload_dir = Path(self.config.get("dynamic.payloads_dir", "./src/dynamic_tester/payloads"))
        for name in ["xss_payloads.txt", "sqli_payloads.txt"]:
            file_path = payload_dir / name
            if file_path.exists():
                with open(file_path, "r") as f:
                    payloads[name] = [line.strip() for line in f if line.strip()]
            else:
                payloads[name] = []
                logger.warning(f"Payload file not found: {file_path}")
        return payloads

    def run(self, target_url: Optional[str] = None) -> List[Finding]:
        """Execute the full dynamic testing workflow."""
        findings = []

        try:
            # Step 1: Set base URL
            if target_url and target_url.startswith(("http://", "https://")):
                self.base_url = target_url
                logger.info(f"Dynamic scanner performing direct hit on: {self.base_url}")
            else:
                target_path = self.context.target_path
                port = self.config.get("dynamic.server.port", 8080)

                self.server_launcher = ServerLauncher(target_path)
                process, base_url = self.server_launcher.start(port=port)

                if not base_url:
                    logger.error("Failed to start local server for dynamic testing.")
                    return findings

                self.base_url = base_url
                self.context.server_process = process
                logger.info(f"Dynamic scanner targeting local instance: {base_url}")

            # Step 2: Crawl to discover URLs
            crawler = Crawler(self.base_url, max_pages=self.max_urls)
            discovered_urls = crawler.crawl()
            logger.info(f"Discovered {len(discovered_urls)} URLs for testing.")
            
            # Update context for reporting (important for "Files Audited" count)
            if hasattr(self.context, 'files_scanned'):
                for url in discovered_urls:
                    self.context.files_scanned.append(Path(urlparse(url).path or "remote_target"))

            # Step 3: Test each URL
            for url in discovered_urls:
                # 3a. Test URL parameters (GET)
                findings.extend(self._test_url_params(url))
                
                # 3b. Test Forms (POST & GET Forms)
                findings.extend(self._test_forms(url))

        except Exception as e:
            logger.error(f"Dynamic scanning error: {e}", exc_info=True)
        finally:
            if self.server_launcher:
                self.server_launcher.stop()

        return findings

    def _test_forms(self, url: str) -> List[Finding]:
        """Discover and test forms on a page."""
        findings = []
        try:
            resp = requests.get(url, timeout=self.timeout)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            
            for form in soup.find_all("form"):
                action = form.get("action", "")
                method = form.get("method", "get").lower()
                target_url = urljoin(url, action)
                
                # Extract inputs
                inputs = {}
                for input_tag in form.find_all(["input", "textarea", "select"]):
                    name = input_tag.get("name")
                    if name:
                        inputs[name] = input_tag.get("value", "test_payload")
                
                if not inputs:
                    continue
                
                logger.info(f"Testing form ({method.upper()}) at {target_url} with {len(inputs)} inputs")
                findings.extend(self._test_payload_injection(target_url, inputs, method))
                    
        except Exception as e:
            logger.debug(f"Error testing forms at {url}: {e}")
            
        return findings

    def _test_payload_injection(self, url: str, params: Dict[str, str], method: str) -> List[Finding]:
        """Test a set of parameters with injection payloads."""
        findings = []
        sqli_payloads = self.payloads.get("sqli_payloads.txt", [])
        xss_payloads = self.payloads.get("xss_payloads.txt", [])
        
        sqli_indicators = [
            "you have an error in your sql syntax", "warning: mysql", "unclosed quotation mark",
            "quoted string not properly terminated", "microsoft ole db provider for sql server",
            "ora-01756", "pg_query", "sqlite3.operationalerror"
        ]

        for param in params:
            # 1. Test SQL Injection
            for payload in sqli_payloads[:3]:  # Reduced to prevent DOS on single-threaded dev server
                test_params = params.copy()
                test_params[param] = payload
                
                try:
                    start_time = time.time()
                    if method == "post":
                        resp = requests.post(url, data=test_params, timeout=self.timeout)
                    else:
                        resp = requests.get(url, params=test_params, timeout=self.timeout)
                    elapsed = time.time() - start_time

                    # Indicator 1: Error messages (Error-based SQLi)
                    response_lower = resp.text.lower()
                    for indicator in sqli_indicators:
                        if indicator in response_lower:
                            findings.append(self._create_finding(
                                "SQL Injection (Dynamic)", 
                                f"SQL error detected in {method.upper()} param '{param}' at {url}", 
                                "critical", url, 
                                {"param": param, "payload": payload, "method": method, "type": "error-based"}
                            ))
                            break
                    
                    # Indicator 2: Time-based (Blind SQLi)
                    if "SLEEP" in payload.upper() and elapsed > 4.5:
                        findings.append(self._create_finding(
                            "Blind SQL Injection (Dynamic)", 
                            f"Time-based SQLi detected in {method.upper()} param '{param}' (Response delayed by {elapsed:.2f}s)", 
                            "critical", url, 
                            {"param": param, "payload": payload, "method": method, "type": "time-based"}
                        ))
                        break
                        
                except requests.RequestException:
                    continue

            # 2. Test Reflected XSS
            for payload in xss_payloads[:3]:  # Reduced for speed
                test_params = params.copy()
                test_params[param] = payload
                try:
                    if method == "post":
                        resp = requests.post(url, data=test_params, timeout=self.timeout)
                    else:
                        resp = requests.get(url, params=test_params, timeout=self.timeout)
                    
                    if payload in resp.text:
                        findings.append(self._create_finding(
                            "Reflected XSS (Dynamic)", 
                            f"XSS payload reflected unescaped in {method.upper()} param '{param}' at {url}", 
                            "high", url, 
                            {"param": param, "payload": payload, "method": method}
                        ))
                        break
                except requests.RequestException:
                    continue
                    
        return findings

    def _create_finding(self, title: str, desc: str, severity: str, url: str, meta: dict) -> Finding:
        """Helper to create Finding objects."""
        return Finding(
            title=title,
            description=desc,
            severity=severity,
            file_path=Path(urlparse(url).path or "remote_target"),
            line_start=None,
            remediation=(
                "Use parameterized queries/prepared statements for SQL. "
                "For XSS, implement context-aware output encoding and a strong Content Security Policy (CSP)."
            ),
            cwe_id="CWE-89" if "SQL" in title else "CWE-79",
            metadata=meta
        )

    def _test_url_params(self, url: str) -> List[Finding]:
        """Test URL query parameters."""
        parsed = urlparse(url)
        query = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        if not query:
            return []
        base_url = urlunparse(parsed._replace(query=""))
        return self._test_payload_injection(base_url, query, "get")