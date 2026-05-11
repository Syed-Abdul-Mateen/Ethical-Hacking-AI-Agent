"""Parser for HTML files to extract scripts, forms, links, and inline event handlers."""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.parsers.base_parser import BaseParser, ParsedFile
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HTMLParser(BaseParser):
    """Parse HTML files extracting security-relevant constructs."""

    # Inline event handler attributes that may contain executable JS
    EVENT_HANDLERS = [
        "onclick", "onload", "onerror", "onmouseover", "onfocus",
        "onblur", "onsubmit", "onchange", "onkeyup", "onkeydown",
        "onmouseout", "ondblclick", "oncontextmenu", "oninput",
    ]

    def __init__(self, config):
        super().__init__(config)
        self.language = "html"

    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        content = self.read_file(file_path)
        if not content:
            return None

        parsed = ParsedFile(file_path, content, self.language)

        metadata: Dict[str, Any] = {
            "scripts": [],
            "inline_scripts": [],
            "forms": [],
            "links": [],
            "iframes": [],
            "event_handlers": [],
            "meta_tags": [],
            "comments": [],
        }

        # Extract <script src="..."> references
        for match in re.finditer(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE):
            metadata["scripts"].append(match.group(1))

        # Extract inline <script>...</script> blocks
        for match in re.finditer(r'<script[^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL):
            body = match.group(1).strip()
            if body:
                metadata["inline_scripts"].append({
                    "content": body,
                    "line": content[:match.start()].count("\n") + 1,
                })

        # Extract <form> elements with action and method
        for match in re.finditer(r'<form\b([^>]*)>', content, re.IGNORECASE):
            attrs = match.group(1)
            action_match = re.search(r'action\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
            method_match = re.search(r'method\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
            metadata["forms"].append({
                "action": action_match.group(1) if action_match else "",
                "method": (method_match.group(1) if method_match else "GET").upper(),
                "line": content[:match.start()].count("\n") + 1,
            })

        # Extract <a href="..."> links
        for match in re.finditer(r'<a[^>]+href\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE):
            metadata["links"].append(match.group(1))

        # Extract <iframe src="...">
        for match in re.finditer(r'<iframe[^>]+src\s*=\s*["\']([^"\']+)["\']', content, re.IGNORECASE):
            metadata["iframes"].append(match.group(1))

        # Extract inline event handlers (e.g., onclick="...")
        for handler in self.EVENT_HANDLERS:
            pattern = rf'{handler}\s*=\s*["\']([^"\']+)["\']'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                metadata["event_handlers"].append({
                    "handler": handler,
                    "value": match.group(1),
                    "line": content[:match.start()].count("\n") + 1,
                })

        # Extract <meta> tags (for security headers, CSRF tokens, etc.)
        for match in re.finditer(
            r'<meta[^>]+(?:name|http-equiv)\s*=\s*["\']([^"\']+)["\'][^>]+content\s*=\s*["\']([^"\']+)["\']',
            content, re.IGNORECASE
        ):
            metadata["meta_tags"].append({
                "name": match.group(1),
                "content": match.group(2),
            })

        # Extract HTML comments (may contain sensitive info)
        for match in re.finditer(r'<!--(.*?)-->', content, re.DOTALL):
            comment = match.group(1).strip()
            if comment:
                metadata["comments"].append({
                    "content": comment,
                    "line": content[:match.start()].count("\n") + 1,
                })

        parsed.metadata = metadata
        return parsed

    def get_supported_extensions(self) -> list:
        return [".html", ".htm", ".xhtml"]
