"""
NPM package.json parser.
"""

import json
from pathlib import Path
from typing import List, Dict


class NPMParser:
    """Parse package.json and package-lock.json."""

    def parse(self, file_path: Path) -> List[Dict[str, str]]:
        """Return list of package names and versions."""
        with open(file_path, "r") as f:
            data = json.load(f)
        deps = []
        # For package.json, we have dependencies and devDependencies
        for section in ["dependencies", "devDependencies"]:
            if section in data:
                for name, version in data[section].items():
                    deps.append({"name": name, "version": version})
        # For package-lock.json, we have packages
        if "packages" in data:
            for pkg, info in data["packages"].items():
                if pkg != "" and "version" in info:
                    # Remove leading node_modules/
                    name = pkg.split("/")[-1] if "/" in pkg else pkg
                    deps.append({"name": name, "version": info["version"]})
        return deps