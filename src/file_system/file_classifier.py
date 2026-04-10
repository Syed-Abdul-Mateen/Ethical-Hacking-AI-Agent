"""Map file extensions to appropriate parser classes."""

import importlib
from pathlib import Path
from typing import Optional, Dict, Type

from src.parsers.base_parser import BaseParser
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


class FileClassifier:
    """
    Determines which parser should handle a given file based on its extension.
    Parsers are loaded dynamically from configuration.
    """

    def __init__(self, config: Config):
        """
        Initialize classifier with parser mappings from config.

        Args:
            config: Agent configuration containing parsers mapping.
        """
        self.config = config
        self._parser_cache: Dict[str, Type[BaseParser]] = {}
        self._load_parsers()

    def _load_parsers(self) -> None:
        """Import parser classes defined in configuration."""
        parser_config = self.config.get("parsers", {})
        for ext, module_path in parser_config.items():
            try:
                # module_path is like "src.parsers.html_parser.HTMLParser"
                module_name, class_name = module_path.rsplit(".", 1)
                module = importlib.import_module(module_name)
                parser_class = getattr(module, class_name)
                if not issubclass(parser_class, BaseParser):
                    logger.error(f"Parser class {class_name} is not a subclass of BaseParser")
                    continue
                self._parser_cache[ext] = parser_class
                logger.debug(f"Loaded parser {class_name} for extension {ext}")
            except (ImportError, AttributeError, ValueError) as e:
                logger.error(f"Failed to load parser for {ext}: {e}")

    def get_parser(self, file_path: Path) -> Optional[BaseParser]:
        """
        Return an instance of the appropriate parser for the given file.

        Args:
            file_path: Path to the file.

        Returns:
            An instance of BaseParser, or None if no parser matches.
        """
        ext = file_path.suffix.lower()
        parser_class = self._parser_cache.get(ext)
        if parser_class:
            try:
                return parser_class(self.config)
            except Exception as e:
                logger.error(f"Error instantiating parser {parser_class.__name__}: {e}")
        return None