"""Detect insecure deserialization via Python pickle."""

import re
from pathlib import Path
from typing import List, Dict

from src.detectors.base_detector import BaseDetector, Finding
from src.parsers.base_parser import ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PythonPickleDetector(BaseDetector):
    """
    Detects insecure usage of Python's pickle module which can lead to
    arbitrary code execution when deserializing untrusted data.
    """

    # Dangerous pickle functions
    DANGEROUS_PATTERNS = [
        (r'\bpickle\.loads?\s*\(', "pickle.load/loads"),
        (r'\bcPickle\.loads?\s*\(', "cPickle.load/loads"),
        (r'\b_pickle\.loads?\s*\(', "_pickle.load/loads"),
        (r'\bshelve\.open\s*\(', "shelve.open (uses pickle internally)"),
        (r'\bjoblib\.load\s*\(', "joblib.load (uses pickle internally)"),
        (r'\btorch\.load\s*\(', "torch.load (uses pickle by default)"),
        (r'\bnumpy\.load\s*\(.*allow_pickle\s*=\s*True', "numpy.load with allow_pickle=True"),
        (r'\byaml\.load\s*\([^)]*\bLoader\s*=\s*yaml\.Loader\b', "yaml.load with unsafe Loader"),
        (r'\byaml\.unsafe_load\s*\(', "yaml.unsafe_load"),
    ]

    # Patterns that indicate data comes from untrusted sources
    UNTRUSTED_SOURCE_PATTERNS = [
        r'request\.',
        r'socket\.',
        r'recv\(',
        r'urlopen\(',
        r'requests\.',
        r'open\(',
        r'sys\.stdin',
        r'input\(',
    ]

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        findings = []

        for file_path, parsed in parsed_data.items():
            if parsed.language != "python":
                continue

            content = parsed.content
            if not content:
                continue

            # Check if pickle/shelve is imported
            has_pickle_import = bool(re.search(
                r'^\s*(?:import|from)\s+(?:pickle|cPickle|_pickle|shelve|joblib)',
                content, re.MULTILINE
            ))
            has_yaml_import = bool(re.search(r'^\s*(?:import|from)\s+yaml', content, re.MULTILINE))
            has_torch_import = bool(re.search(r'^\s*(?:import|from)\s+torch', content, re.MULTILINE))
            has_numpy_import = bool(re.search(r'^\s*(?:import|from)\s+numpy', content, re.MULTILINE))

            if not (has_pickle_import or has_yaml_import or has_torch_import or has_numpy_import):
                continue

            for line_num, line in enumerate(parsed.lines, start=1):
                for pattern, func_name in self.DANGEROUS_PATTERNS:
                    if re.search(pattern, line):
                        # Check surrounding context for untrusted data sources
                        context_start = max(0, line_num - 6)
                        context_end = min(len(parsed.lines), line_num + 3)
                        context_block = "".join(parsed.lines[context_start:context_end])

                        has_untrusted_source = any(
                            re.search(up, context_block)
                            for up in self.UNTRUSTED_SOURCE_PATTERNS
                        )

                        severity = "critical" if has_untrusted_source else "high"
                        snippet = parsed.get_snippet(line_num, context_lines=2)

                        finding = Finding(
                            title="Insecure Deserialization (Pickle)",
                            description=(
                                f"Usage of '{func_name}' detected. Deserializing untrusted data with pickle "
                                f"can lead to arbitrary code execution. "
                                f"{'The data appears to come from an untrusted source.' if has_untrusted_source else ''}"
                            ),
                            severity=severity,
                            file_path=file_path,
                            line_start=line_num,
                            code_snippet=snippet,
                            remediation=(
                                "Avoid using pickle to deserialize untrusted data. Use safer formats like JSON "
                                "or MessagePack. If pickle is required, use a restricted unpickler with "
                                "allowlisted classes (RestrictedUnpickler pattern). For PyTorch, use "
                                "torch.load(..., weights_only=True)."
                            ),
                            cwe_id="CWE-502",
                        )
                        findings.append(finding)
                        break  # One finding per line

        return findings
