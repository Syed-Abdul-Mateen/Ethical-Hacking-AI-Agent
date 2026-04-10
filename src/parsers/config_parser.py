"""Parsers for configuration files: JSON, YAML, XML, .env."""

import json
import yaml
import re
from pathlib import Path
from typing import Optional, Dict, Any

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class JSONParser(BaseParser):
    """Parse JSON files."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "json"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)
        try:
            data = json.loads(content)
            parsed.ast = data
            parsed.metadata = {"keys": list(data.keys()) if isinstance(data, dict) else []}
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in {file_path}: {e}")
        return parsed


class YAMLParser(BaseParser):
    """Parse YAML files."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "yaml"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)
        try:
            data = yaml.safe_load(content)
            parsed.ast = data
            parsed.metadata = {"keys": list(data.keys()) if isinstance(data, dict) else []}
        except yaml.YAMLError as e:
            logger.warning(f"Invalid YAML in {file_path}: {e}")
        return parsed


class XMLParser(BaseParser):
    """Parse XML files using lxml."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "xml"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)
        try:
            from lxml import etree
            tree = etree.fromstring(content.encode('utf-8'))
            parsed.ast = tree
            parsed.metadata = {"root_tag": tree.tag}
        except Exception as e:
            logger.warning(f"Error parsing XML {file_path}: {e}")
        return parsed


class EnvParser(BaseParser):
    """Parse .env files (key=value)."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "env"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)
        env_vars = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
        parsed.metadata = {"variables": env_vars}
        return parsed