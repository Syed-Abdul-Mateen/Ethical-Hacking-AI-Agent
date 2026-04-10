"""
Java Maven pom.xml parser.
"""

from pathlib import Path
from typing import List, Dict
import xml.etree.ElementTree as ET


class MavenParser:
    """Parse pom.xml."""

    def parse(self, file_path: Path) -> List[Dict[str, str]]:
        deps = []
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Namespace handling
        ns = {"mvn": "http://maven.apache.org/POM/4.0.0"}
        for dep in root.findall(".//mvn:dependency", ns):
            group_id = dep.find("mvn:groupId", ns)
            artifact_id = dep.find("mvn:artifactId", ns)
            version = dep.find("mvn:version", ns)
            if group_id is not None and artifact_id is not None and version is not None:
                name = f"{group_id.text}:{artifact_id.text}"
                deps.append({"name": name, "version": version.text})
        return deps