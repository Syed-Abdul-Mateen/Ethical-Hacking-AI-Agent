"""Orchestrator package: AI brain of the agent.

Uses lazy imports to prevent circular import chains with the detectors package.
"""

from .context import ScanContext
from .exceptions import (
    OrchestratorError,
    ScanInterrupted,
    ConfigurationError,
    DetectorError,
)


def __getattr__(name):
    """Lazy import for Agent and DetectorRegistry to avoid circular imports."""
    if name == "Agent":
        from .agent import Agent
        return Agent
    if name == "DetectorRegistry":
        from .registry import DetectorRegistry
        return DetectorRegistry
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Agent",
    "ScanContext",
    "DetectorRegistry",
    "OrchestratorError",
    "ScanInterrupted",
    "ConfigurationError",
    "DetectorError",
]