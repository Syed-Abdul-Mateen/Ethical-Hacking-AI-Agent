"""Detect hardcoded secrets such as API keys, passwords, and tokens in source code."""

import re
from pathlib import Path
from typing import List, Dict, Any

from src.detectors.base_detector import BaseDetector, Finding
from src.parsers.base_parser import ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HardcodedSecretsDetector(BaseDetector):
    """
    Detects hardcoded secrets in source code including:
    - API keys and tokens
    - Passwords assigned to variables
    - Connection strings with embedded credentials
    - Private keys and certificates
    """

    SECRET_PATTERNS = [
        # Generic API key patterns
        (r'(?:api[_-]?key|apikey)\s*[:=]\s*["\']([^"\']{8,})["\']', "API Key", "CWE-798"),
        # Generic secret/token patterns
        (r'(?:secret|token|auth[_-]?token|access[_-]?token)\s*[:=]\s*["\']([^"\']{8,})["\']',
         "Secret/Token", "CWE-798"),
        # Password assignments
        (r'(?:password|passwd|pwd|pass)\s*[:=]\s*["\']([^"\']{4,})["\']',
         "Hardcoded Password", "CWE-259"),
        # AWS keys
        (r'(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}', "AWS Access Key", "CWE-798"),
        # AWS Secret key
        (r'(?:aws[_-]?secret[_-]?access[_-]?key)\s*[:=]\s*["\']([^"\']{20,})["\']',
         "AWS Secret Key", "CWE-798"),
        # GitHub tokens
        (r'gh[pousr]_[A-Za-z0-9_]{36,}', "GitHub Token", "CWE-798"),
        # Slack tokens
        (r'xox[baprs]-[0-9]{10,}-[0-9A-Za-z]{10,}', "Slack Token", "CWE-798"),
        # Generic connection strings with password
        (r'(?:mongodb|mysql|postgresql|redis|amqp)://[^:]+:([^@]+)@',
         "Connection String with Password", "CWE-798"),
        # Private key headers
        (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', "Private Key", "CWE-321"),
        # Bearer token in headers
        (r'["\']Bearer\s+[A-Za-z0-9\-._~+/]+=*["\']', "Bearer Token", "CWE-798"),
        # JWT tokens (three base64 segments separated by dots)
        (r'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}',
         "JWT Token", "CWE-798"),
    ]

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []

        for file_path, parsed in parsed_data.items():
            content = parsed.content
            if not content:
                continue

            for pattern, secret_type, cwe_id in self.SECRET_PATTERNS:
                try:
                    for match in re.finditer(pattern, content, re.IGNORECASE):
                        line_num = content[:match.start()].count("\n") + 1
                        snippet = parsed.get_snippet(line_num, context_lines=1)

                        # Mask the actual secret in the description
                        matched_text = match.group(0)
                        masked = matched_text[:8] + "..." + matched_text[-4:] if len(matched_text) > 16 else "***"

                        finding = Finding(
                            title=f"Hardcoded {secret_type}",
                            description=(
                                f"A {secret_type.lower()} appears to be hardcoded in source code. "
                                f"Matched pattern: {masked}"
                            ),
                            severity="high",
                            file_path=file_path,
                            line_start=line_num,
                            code_snippet=snippet,
                            remediation=(
                                "Remove hardcoded secrets from source code. Use environment variables, "
                                "a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault), "
                                "or encrypted configuration files instead."
                            ),
                            cwe_id=cwe_id,
                        )
                        findings.append(finding)
                except re.error as e:
                    logger.warning(f"Regex error for pattern '{secret_type}': {e}")

        return findings
