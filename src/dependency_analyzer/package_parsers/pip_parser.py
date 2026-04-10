"""
Python requirements.txt parser.
"""

from pathlib import Path
from typing import List, Dict
import re


class PipParser:
    """Parse requirements.txt or Pipfile.lock."""

    def parse(self, file_path: Path) -> List[Dict[str, str]]:
        deps = []
        if file_path.suffix == ".txt":
            # requirements.txt format
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Extract package name and version
                        # Format: package==version or package>=version
                        match = re.match(r'([a-zA-Z0-9_-]+)(?:[=<>]+)([^;]+)', line)
                        if match:
                            deps.append({"name": match.group(1), "version": match.group(2)})
                        else:
                            # Just package name
                            deps.append({"name": line, "version": "unknown"})
        elif file_path.name == "Pipfile.lock":
            import json
            with open(file_path, "r") as f:
                data = json.load(f)
            for pkg, info in data.get("default", {}).items():
                deps.append({"name": pkg, "version": info.get("version", "unknown")})
        return deps