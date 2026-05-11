"""
YAML-based detection engine.
Allows defining security rules in YAML format for easy extensibility.
"""

import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext
from src.parsers.base_parser import ParsedFile
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RuleEngine(BaseDetector):
    """
    Executes custom security rules defined in YAML.
    Rules support regex patterns, multi-line matching, and language-specific filtering.
    """

    def __init__(self, config: Config, context: ScanContext):
        super().__init__(config, context)
        # Use a safe default for rules_dir if not in config
        self.rules_dir = Path(config.get("detectors.rules_dir", "./configs/rules"))
        self.rules: List[Dict[str, Any]] = []
        self._load_rules()

    def _load_rules(self) -> None:
        """Load all YAML rules from the rules directory."""
        if not self.rules_dir.exists():
            logger.warning(f"Rules directory not found: {self.rules_dir}")
            return

        for rule_file in self.rules_dir.glob("*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    rule_data = yaml.safe_load(f)
                    if rule_data and self._validate_rule(rule_data):
                        self.rules.append(rule_data)
                        logger.debug(f"Loaded custom rule: {rule_data.get('id')}")
            except Exception as e:
                logger.error(f"Failed to load rule {rule_file}: {e}")

        logger.info(f"Rule Engine: {len(self.rules)} custom rules loaded.")

    def _validate_rule(self, rule: Dict[str, Any]) -> bool:
        """Ensure the rule has all required fields."""
        required = ["id", "title", "severity", "patterns"]
        return all(k in rule for k in required)

    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        """Execute all loaded rules against the parsed files."""
        all_findings = []

        for file_path, parsed_file in parsed_data.items():
            for rule in self.rules:
                # Filter by language if specified in rule
                if "languages" in rule and parsed_file.language not in rule["languages"]:
                    continue

                findings = self._apply_rule(rule, parsed_file)
                all_findings.extend(findings)

        return all_findings

    def _apply_rule(self, rule: Dict[str, Any], parsed_file: ParsedFile) -> List[Finding]:
        """Apply a single rule to a file."""
        findings = []
        content = parsed_file.content
        
        # Determine patterns to check
        patterns = rule.get("patterns", [])
        if not patterns:
            return []

        for pattern_data in patterns:
            regex_str = pattern_data.get("regex")
            if not regex_str:
                continue

            # Compile with multiline support
            flags = re.MULTILINE | re.IGNORECASE
            try:
                for match in re.finditer(regex_str, content, flags):
                    line_start = content[:match.start()].count("\n") + 1
                    line_end = content[:match.end()].count("\n") + 1
                    
                    finding = Finding(
                        title=rule["title"],
                        description=rule.get("description", ""),
                        severity=rule["severity"],
                        file_path=parsed_file.path,
                        line_start=line_start,
                        line_end=line_end,
                        code_snippet=parsed_file.get_snippet(line_start),
                        remediation=rule.get("remediation"),
                        cwe_id=rule.get("cwe"),
                        metadata={
                            "rule_id": rule["id"],
                            "match": match.group(0)[:100]
                        }
                    )
                    findings.append(finding)
            except Exception as e:
                logger.error(f"Regex error in rule {rule['id']}: {e}")

        return findings
