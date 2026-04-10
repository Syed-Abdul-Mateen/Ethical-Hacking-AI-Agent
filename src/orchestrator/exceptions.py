"""Custom exceptions for the orchestrator and overall agent."""

class OrchestratorError(Exception):
    """Base exception for orchestrator-related errors."""
    pass


class ScanInterrupted(OrchestratorError):
    """Raised when the user interrupts the scan (Ctrl+C)."""
    pass


class ConfigurationError(OrchestratorError):
    """Raised when there is an issue with the configuration."""
    pass


class DetectorError(OrchestratorError):
    """Raised when a detector fails to execute."""
    pass