"""Remove duplicate findings based on file path, line number, and rule."""

from typing import List, Set, Tuple, Any

from src.detectors.base_detector import Finding


class Deduplicator:
    """Deduplicate findings using a key derived from file path, line numbers, and title."""

    def __init__(self):
        pass

    def deduplicate(self, findings: List[Finding]) -> List[Finding]:
        """Return a list of unique findings."""
        seen: Set[Tuple[str, int, int, str]] = set()
        unique = []
        for f in findings:
            key = (
                str(f.file_path),
                f.line_start or 0,
                f.line_end or 0,
                f.title,
            )
            if key not in seen:
                seen.add(key)
                unique.append(f)
        return unique