"""Parser for JavaScript and TypeScript files using esprima."""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any

import esprima

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class JavaScriptParser(BaseParser):
    """Parse JavaScript files (ES5/ES6+)."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "javascript"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)

        try:
            # Parse to AST
            ast = esprima.parseScript(content, {"loc": True, "range": True})
            parsed.ast = ast

            # Extract metadata
            metadata = {
                "imports": [],
                "exports": [],
                "functions": [],
                "dangerous_functions": [],  # eval, document.write, etc.
                "api_calls": [],
            }

            # Simple recursive walker for AST
            def walk(node):
                if node is None or not hasattr(node, "type"):
                    return
                
                if node.type == "ImportDeclaration":
                    metadata["imports"].append(node.source.value)
                elif node.type == "ExportNamedDeclaration" and node.source:
                    metadata["exports"].append(node.source.value)
                elif node.type == "FunctionDeclaration":
                    metadata["functions"].append(node.id.name if node.id else "anonymous")
                elif node.type == "CallExpression":
                    if node.callee.type == "Identifier":
                        name = node.callee.name
                        if name in ("eval", "setTimeout", "setInterval"):
                            metadata["dangerous_functions"].append(name)
                        elif name in ("fetch", "XMLHttpRequest", "axios"):
                            metadata["api_calls"].append(name)

                # Recursively walk attributes
                for key in dir(node):
                    if key.startswith("_") or key in ("type", "loc", "range"):
                        continue
                    value = getattr(node, key)
                    if isinstance(value, list):
                        for item in value:
                            if hasattr(item, "type"):
                                walk(item)
                    elif hasattr(value, "type"):
                        walk(value)

            walk(ast)

            parsed.metadata = metadata

        except esprima.Error as e:
            logger.warning(f"Esprima error parsing {file_path}: {e}")
            # Still return parsed content

        return parsed


class TypeScriptParser(JavaScriptParser):
    """Parse TypeScript files using esprima (fallback)."""

    def __init__(self, config):
        super().__init__(config)
        self.language = "typescript"

    # TypeScript-specific features could be added here, but for simplicity we reuse JS parser.