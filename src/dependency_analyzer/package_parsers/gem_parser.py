"""
Ruby Gemfile.lock parser.
"""

from pathlib import Path
from typing import List, Dict
import re


class GemParser:
    """Parse Gemfile.lock."""

    def parse(self, file_path: Path) -> List[Dict[str, str]]:
        deps = []
        with open(file_path, "r") as f:
            content = f.read()
        # Simple regex: find lines like "gem_name (version)"
        pattern = re.compile(r'^([a-zA-Z0-9_-]+)\s*\(([0-9.]+)\)', re.MULTILINE)
        for match in pattern.finditer(content):
            deps.append({"name": match.group(1), "version": match.group(2)})
        return deps