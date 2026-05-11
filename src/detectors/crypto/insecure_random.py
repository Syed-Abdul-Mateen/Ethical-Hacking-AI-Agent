"""Detect insecure random number generation in security-sensitive contexts."""

import re
from pathlib import Path
from typing import List, Dict

from src.detectors.base_detector import BaseDetector, Finding
from src.parsers.base_parser import ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class InsecureRandomDetector(BaseDetector):
    """
    Detects usage of non-cryptographic random number generators
    in contexts where cryptographic randomness is required (tokens, keys, nonces).
    """

    # Map of language to their insecure random patterns
    INSECURE_PATTERNS = {
        "python": [
            (r'\brandom\.(random|randint|randrange|choice|shuffle|sample)\s*\(', "random module"),
        ],
        "javascript": [
            (r'\bMath\.random\s*\(', "Math.random()"),
        ],
        "php": [
            (r'\brand\s*\(', "rand()"),
            (r'\bmt_rand\s*\(', "mt_rand()"),
            (r'\barray_rand\s*\(', "array_rand()"),
        ],
        "java": [
            (r'\bnew\s+Random\s*\(', "java.util.Random"),
            (r'\bMath\.random\s*\(', "Math.random()"),
        ],
        "csharp": [
            (r'\bnew\s+Random\s*\(', "System.Random"),
        ],
        "ruby": [
            (r'\brand\s*\(', "rand()"),
            (r'\bRandom\.new', "Random.new"),
        ],
        "go": [
            (r'\bmath/rand\b', "math/rand import"),
            (r'\brand\.(Intn|Int63|Float64)\s*\(', "math/rand function"),
        ],
    }

    # Contextual keywords that indicate security-sensitive usage
    SECURITY_CONTEXT = [
        "token", "secret", "key", "password", "nonce", "salt", "session",
        "csrf", "auth", "otp", "verification", "reset", "confirm",
    ]

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []

        for file_path, parsed in parsed_data.items():
            patterns = self.INSECURE_PATTERNS.get(parsed.language, [])
            if not patterns:
                continue

            content = parsed.content
            if not content:
                continue

            for line_num, line in enumerate(parsed.lines, start=1):
                for pattern, func_name in patterns:
                    if re.search(pattern, line):
                        # Check if the surrounding context suggests security usage
                        context_start = max(0, line_num - 4)
                        context_end = min(len(parsed.lines), line_num + 3)
                        context_block = "".join(parsed.lines[context_start:context_end]).lower()

                        is_security_context = any(
                            keyword in context_block for keyword in self.SECURITY_CONTEXT
                        )

                        severity = "high" if is_security_context else "medium"
                        snippet = parsed.get_snippet(line_num, context_lines=2)

                        finding = Finding(
                            title="Insecure Random Number Generation",
                            description=(
                                f"Usage of non-cryptographic PRNG '{func_name}' detected. "
                                f"{'This appears to be in a security-sensitive context. ' if is_security_context else ''}"
                                f"Non-cryptographic PRNGs produce predictable output and must not be used "
                                f"for security tokens, keys, or nonces."
                            ),
                            severity=severity,
                            file_path=file_path,
                            line_start=line_num,
                            code_snippet=snippet,
                            remediation=self._get_remediation(parsed.language),
                            cwe_id="CWE-338",
                        )
                        findings.append(finding)

        return findings

    @staticmethod
    def _get_remediation(language: str) -> str:
        """Return language-specific remediation advice."""
        advice = {
            "python": "Use `secrets` module (e.g., secrets.token_hex()) or `os.urandom()` for cryptographic randomness.",
            "javascript": "Use `crypto.getRandomValues()` (browser) or `crypto.randomBytes()` (Node.js) instead.",
            "php": "Use `random_bytes()` or `random_int()` which use cryptographically secure PRNGs.",
            "java": "Use `java.security.SecureRandom` instead of `java.util.Random`.",
            "csharp": "Use `System.Security.Cryptography.RandomNumberGenerator` instead of `System.Random`.",
            "ruby": "Use `SecureRandom.hex()` or `SecureRandom.random_bytes()` from the securerandom library.",
            "go": "Use `crypto/rand` package instead of `math/rand`.",
        }
        return advice.get(language, "Use a cryptographically secure PRNG provided by your language's standard library.")
