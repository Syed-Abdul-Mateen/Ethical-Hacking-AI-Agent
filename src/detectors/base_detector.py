"""Abstract base class for all vulnerability detectors."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.orchestrator.context import ScanContext
from src.utils.config import Config
from src.utils.logger import get_logger
from src.parsers.base_parser import ParsedFile

logger = get_logger(__name__)


class Finding:
    """
    Represents a single vulnerability finding.
    """

    def __init__(
        self,
        title: str,
        description: str,
        severity: str,  # "critical", "high", "medium", "low", "info"
        file_path: Path,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        code_snippet: Optional[str] = None,
        remediation: Optional[str] = None,
        cwe_id: Optional[str] = None,
        cvss_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.title = title
        self.description = description
        self.severity = severity
        self.file_path = file_path
        self.line_start = line_start
        self.line_end = line_end
        self.code_snippet = code_snippet
        self.remediation = remediation
        self.cwe_id = cwe_id
        self.cvss_score = cvss_score
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialisation."""
        return {
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "file_path": str(self.file_path),
            "line_start": self.line_start,
            "line_end": self.line_end,
            "code_snippet": self.code_snippet,
            "remediation": self.remediation,
            "cwe_id": self.cwe_id,
            "cvss_score": self.cvss_score,
            "metadata": self.metadata,
        }


class BaseDetector(ABC):
    """
    Abstract base class for vulnerability detectors.
    Subclasses must implement the `run` method.
    """

    def __init__(self, config: Config, context: ScanContext):
        self.config = config
        self.context = context
        self.name = self.__class__.__name__.replace("Detector", "")

    @abstractmethod
    def run(self, parsed_data: Dict[Path, ParsedFile]) -> List[Finding]:
        """
        Run the detector on parsed files.

        Args:
            parsed_data: Mapping from file paths to ParsedFile objects.

        Returns:
            List of Finding objects.
        """
        pass

    def _get_cwe_info(self, cwe_id: str) -> Dict[str, str]:
        """Retrieve CWE information from the knowledge base."""
        # Placeholder - will be implemented when knowledge base is ready
        return {"description": "", "remediation": ""}