"""Planner decides which detectors to run based on context and configuration."""

import importlib
from typing import List, Type

from src.orchestrator.context import ScanContext
from src.detectors.base_detector import BaseDetector
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


class Planner:
    """
    Determines which detector classes should be executed during a scan.
    Uses configuration (enabled/disabled detectors) and optionally the file types present.
    """

    def __init__(self, config: Config):
        """
        Initialize the planner.

        Args:
            config: Agent configuration.
        """
        self.config = config
        self._detector_cache = {}

    def plan(self, context: ScanContext) -> List[Type[BaseDetector]]:
        """
        Return a list of detector classes to run for the given context.

        Args:
            context: Current scan context (contains parsed data, etc.)

        Returns:
            List of detector classes (subclasses of BaseDetector).
        """
        enabled_names = self.config.get("detectors.enabled", [])
        if not enabled_names:
            logger.warning("No detectors enabled in configuration.")
            return []

        detector_classes = []
        for name in enabled_names:
            cls = self._load_detector(name)
            if cls:
                detector_classes.append(cls)

        # Optionally filter detectors based on parsed file types
        # (e.g., only run PHP detectors if PHP files are present)
        # This is a placeholder for more advanced logic.
        if context.parsed_data:
            # For now, we run all enabled detectors regardless of file types.
            # Future improvement: implement file-type-based filtering.
            pass

        logger.debug(f"Planner selected {len(detector_classes)} detectors.")
        return detector_classes

    def _load_detector(self, detector_name: str) -> Type[BaseDetector]:
        """
        Dynamically import a detector class by its configuration name.

        Args:
            detector_name: e.g., "injection.sql_injection"

        Returns:
            Detector class, or None if not found.
        """
        if detector_name in self._detector_cache:
            return self._detector_cache[detector_name]

        # Convert "injection.sql_injection" to module path "src.detectors.injection.sql_injection"
        parts = detector_name.split(".")
        module_path = f"src.detectors.{'.'.join(parts)}"
        class_name = self._to_class_name(parts[-1])

        try:
            module = importlib.import_module(module_path)
            detector_class = getattr(module, class_name)
            if not issubclass(detector_class, BaseDetector):
                logger.error(f"Class {class_name} in {module_path} is not a subclass of BaseDetector")
                return None
            self._detector_cache[detector_name] = detector_class
            return detector_class
        except (ImportError, AttributeError) as e:
            logger.error(f"Could not load detector {detector_name}: {e}")
            return None

    def _to_class_name(self, name: str) -> str:
        """Convert snake_case to PascalCase (e.g., sql_injection -> SQLInjectionDetector)."""
        # For simplicity, we assume detector class names are PascalCase with "Detector" suffix.
        # e.g., sql_injection -> SQLInjectionDetector
        parts = name.split("_")
        pascal = "".join(p.capitalize() for p in parts)
        return f"{pascal}Detector"