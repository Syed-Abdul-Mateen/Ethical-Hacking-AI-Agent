"""
PHP Composer parser.
"""

import json
from pathlib import Path
from typing import List, Dict


class ComposerParser:
    """Parse composer.json and composer.lock."""

    def parse(self, file_path: Path) -> List[Dict[str, str]]:
        deps = []
        with open(file_path, "r") as f:
            data = json.load(f)
        if "require" in data:
            for name, version in data["require"].items():
                if name != "php":
                    deps.append({"name": name, "version": version})
        if "packages" in data:
            for pkg in data["packages"]:
                deps.append({"name": pkg["name"], "version": pkg["version"]})
        return deps