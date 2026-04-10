"""Recursively walk a directory and return files, respecting ignore patterns."""

from pathlib import Path
from typing import List, Optional

import pathspec

from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


class FileWalker:
    """
    Traverses a directory tree and returns all files, optionally filtering by ignore patterns.
    """

    def __init__(self, config: Config):
        """
        Initialize with configuration.

        Args:
            config: Agent configuration containing walker settings.
        """
        self.config = config
        self.ignore_patterns = config.get("walker.ignore_patterns", [])
        self.include_extensions = config.get("walker.include_extensions", None)
        self.max_file_size_mb = config.get("agent.max_file_size_mb", 10)
        self.follow_symlinks = config.get("agent.follow_symlinks", False)

        # Precompile ignore patterns using pathspec
        self.ignore_spec = pathspec.PathSpec.from_lines(
            pathspec.patterns.GitWildMatchPattern, self.ignore_patterns
        ) if self.ignore_patterns else None

    def walk(self, root: Path) -> List[Path]:
        """
        Recursively walk the root directory and return a list of file paths.

        Args:
            root: Starting directory.

        Returns:
            Sorted list of absolute file paths.
        """
        root = Path(root).resolve()
        if not root.is_dir():
            logger.error(f"Root is not a directory: {root}")
            return []

        files = []
        for entry in root.rglob("*"):
            if not entry.is_file():
                continue

            # Skip if we don't follow symlinks and this is a symlink
            if not self.follow_symlinks and entry.is_symlink():
                logger.debug(f"Skipping symlink: {entry}")
                continue

            # Check file size
            try:
                size = entry.stat().st_size / (1024 * 1024)  # MB
                if size > self.max_file_size_mb:
                    logger.debug(f"Skipping oversized file ({size:.2f} MB): {entry}")
                    continue
            except OSError as e:
                logger.warning(f"Cannot stat {entry}: {e}")
                continue

            # Check ignore patterns
            rel_path = entry.relative_to(root)
            if self.ignore_spec and self.ignore_spec.match_file(str(rel_path)):
                logger.debug(f"Ignoring pattern-matched file: {rel_path}")
                continue

            # Filter by extensions if specified
            if self.include_extensions:
                if entry.suffix.lower() not in self.include_extensions:
                    continue

            files.append(entry)

        logger.info(f"Found {len(files)} files after filtering.")
        return sorted(files)