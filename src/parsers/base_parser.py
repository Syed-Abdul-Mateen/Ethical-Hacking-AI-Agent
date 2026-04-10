"""Abstract base class for all language-specific parsers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Dict, List

from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ParsedFile:
    """
    Container for parsed file data.
    Detectors will operate on instances of this class.
    """

    def __init__(self, path: Path, content: str, language: str):
        self.path = path
        self.content = content
        self.language = language
        self.lines: List[str] = content.splitlines(keepends=True) if content else []
        self.ast: Optional[Any] = None          # Abstract syntax tree (if parser provides)
        self.metadata: Dict[str, Any] = {}      # Additional info (e.g., comments, imports)

    def get_line(self, line_number: int) -> str:
        """Return the content of a specific line (1-indexed)."""
        if 1 <= line_number <= len(self.lines):
            return self.lines[line_number - 1]
        return ""

    def get_snippet(self, line_number: int, context_lines: int = 2) -> str:
        """Return a snippet of code around the given line."""
        start = max(0, line_number - 1 - context_lines)
        end = min(len(self.lines), line_number + context_lines)
        snippet = "".join(self.lines[start:end])
        return snippet


class BaseParser(ABC):
    """Abstract base class for file parsers."""

    def __init__(self, config: Config):
        self.config = config
        self.language = self.__class__.__name__.replace("Parser", "").lower()

    @abstractmethod
    def parse(self, file_path: Path) -> Optional[ParsedFile]:
        """
        Parse the given file and return a ParsedFile object.

        Args:
            file_path: Path to the file.

        Returns:
            ParsedFile instance containing structured data, or None if parsing failed.
        """
        pass

    def read_file(self, file_path: Path) -> Optional[str]:
        """Read a file with automatic encoding detection."""
        try:
            import chardet
            with open(file_path, "rb") as f:
                raw = f.read()
                encoding = chardet.detect(raw)["encoding"] or "utf-8"
            return raw.decode(encoding, errors="replace")
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return None