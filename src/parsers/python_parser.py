"""Parser for Python files using AST."""

import ast
import re
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PythonParser(BaseParser):
    """Parse Python files using the built-in ast module."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "python"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)

        try:
            tree = ast.parse(content)
            parsed.ast = tree

            metadata = {
                "imports": [],
                "functions": [],
                "classes": [],
                "decorators": [],
                "dangerous_calls": [],  # eval, exec, __import__
                "sql_queries": [],
            }

            # Walk AST
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        metadata["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        metadata["imports"].append(f"{module}.{alias.name}")
                elif isinstance(node, ast.FunctionDef):
                    metadata["functions"].append(node.name)
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            metadata["decorators"].append(decorator.id)
                elif isinstance(node, ast.ClassDef):
                    metadata["classes"].append(node.name)
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ("eval", "exec", "__import__"):
                            metadata["dangerous_calls"].append(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        if node.func.attr in ("execute", "executemany") and isinstance(node.func.value, ast.Name):
                            if node.func.value.id in ("cursor", "conn"):
                                # Potential SQL query
                                if node.args:
                                    metadata["sql_queries"].append(ast.unparse(node.args[0]))

            parsed.metadata = metadata

        except SyntaxError as e:
            logger.warning(f"Syntax error parsing Python {file_path}: {e}")
            # Still return parsed with content only

        return parsed