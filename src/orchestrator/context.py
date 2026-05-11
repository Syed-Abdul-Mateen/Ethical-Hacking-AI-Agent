"""Holds all data and state for a single scan."""

import threading
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
    original_target: Optional[str] = None

    @property
    def files_scanned_count(self) -> int:
        """Return the number of files scanned."""
        return len(self.files_scanned)

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

    # Threading lock for safe updates
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add_error(self, component: str, message: str) -> None:
        """Record an error that occurred during the scan."""
        with self._lock:
            self.errors.append({"component": component, "message": message})

    def add_finding(self, finding: Any) -> None:
        """Add a finding in a thread-safe manner."""
        with self._lock:
            self.findings.append(finding)