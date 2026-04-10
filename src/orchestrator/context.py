"""Holds all data and state for a single scan."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.utils.config import Config


@dataclass
class ScanContext:
    """
    Container for all information related to a scan.
    Passed between modules to share state.
    """

    # Input
    target_path: Path
    config: Config

    # Output
    output_dir: Optional[Path] = None
    report_paths: Dict[str, Path] = field(default_factory=dict)

    # Scan data
    files_scanned: List[Path] = field(default_factory=list)
    parsed_data: Dict[Path, Any] = field(default_factory=dict)  # parser output per file

    # Findings
    findings: List[Any] = field(default_factory=list)           # detector findings
    vulnerable_dependencies: List[Any] = field(default_factory=list)
    secrets_findings: List[Any] = field(default_factory=list)
    dynamic_findings: List[Any] = field(default_factory=list)

    # Scan metadata
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    interrupted: bool = False
    errors: List[Dict[str, str]] = field(default_factory=list)  # {component: error_msg}

    # Dynamic testing
    dynamic_enabled: bool = False
    server_process: Optional[Any] = None   # Popen object if server started

    # Temporary directory for this scan
    temp_dir: Optional[Path] = None

    def add_error(self, component: str, message: str) -> None:
        """Record an error that occurred during the scan."""
        self.errors.append({"component": component, "message": message})