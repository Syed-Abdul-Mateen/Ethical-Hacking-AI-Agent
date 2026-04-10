"""Handle patterns to skip during file traversal (optional)."""

from pathlib import Path
from typing import List, Optional

import pathspec


class IgnoreList:
    """
    Load and apply ignore patterns from a file (e.g., .ehaiignore) similar to .gitignore.
    """

    def __init__(self, ignore_file: Optional[Path] = None):
        """
        Initialize with an optional ignore file.

        Args:
            ignore_file: Path to a file containing ignore patterns (one per line).
        """
        self.ignore_file = ignore_file
        self.spec = None
        if ignore_file and ignore_file.exists():
            with open(ignore_file, "r") as f:
                lines = f.readlines()
            self.spec = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern, lines
            )

    def should_ignore(self, path: Path, root: Path) -> bool:
        """
        Check if a path should be ignored.

        Args:
            path: Absolute path to the file/directory.
            root: Root directory of the scan (for relative path calculation).

        Returns:
            True if the path matches any ignore pattern.
        """
        if not self.spec:
            return False
        rel = path.relative_to(root)
        return self.spec.match_file(str(rel))