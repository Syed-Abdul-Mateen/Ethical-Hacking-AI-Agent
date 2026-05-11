"""
Plugin registry for auto-discovering and managing detector classes.
Supports loading detectors from the built-in detectors directory and
custom directories specified in configuration.
"""

import importlib
import pkgutil
import inspect
from pathlib import Path
from typing import List, Type, Dict, Optional

from src.detectors.base_detector import BaseDetector
from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)


class DetectorRegistry:
    """
    Auto-discover and register all detector classes from the detectors package.

    Usage:
        registry = DetectorRegistry(config)
        all_detectors = registry.get_all()
        enabled = registry.get_enabled()
    """

    def __init__(self, config: Config):
        self.config = config
        self._registry: Dict[str, Type[BaseDetector]] = {}
        self._discover_detectors()

    def _discover_detectors(self) -> None:
        """
        Walk the src.detectors package tree and register all BaseDetector subclasses.
        """
        import src.detectors as detectors_pkg

        package_path = Path(detectors_pkg.__file__).parent

        for importer, modname, ispkg in pkgutil.walk_packages(
            path=[str(package_path)],
            prefix="src.detectors.",
            onerror=lambda name: logger.debug(f"Could not import {name}"),
        ):
            if ispkg:
                continue  # We only want modules, not sub-packages themselves

            try:
                module = importlib.import_module(modname)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (
                        issubclass(obj, BaseDetector)
                        and obj is not BaseDetector
                        and not inspect.isabstract(obj)
                    ):
                        # Build a registry key like "injection.sql_injection.SqlInjectionDetector"
                        relative_module = modname.replace("src.detectors.", "")
                        registry_key = f"{relative_module}.{name}"
                        self._registry[registry_key] = obj
                        logger.debug(f"Registered detector: {registry_key}")

            except Exception as e:
                logger.warning(f"Failed to import detector module {modname}: {e}")

        logger.info(f"Detector registry: {len(self._registry)} detectors discovered.")

    def get_all(self) -> Dict[str, Type[BaseDetector]]:
        """Return all discovered detector classes."""
        return self._registry.copy()

    def get_enabled(self) -> List[Type[BaseDetector]]:
        """
        Return detector classes that are enabled in configuration.

        The config format is:
            detectors.enabled:
              - "injection.sql_injection"
              - "xss.reflected_xss"

        This matches against the module path (without class name).
        """
        enabled_names = self.config.get("detectors.enabled", [])
        if not enabled_names:
            logger.warning("No detectors enabled in configuration. Returning all discovered detectors.")
            return list(self._registry.values())

        enabled_classes = []
        for name in enabled_names:
            # Try to find matching detectors
            matched = False
            for key, cls in self._registry.items():
                # Match by module path (e.g., "injection.sql_injection" matches
                # "injection.sql_injection.SqlInjectionDetector")
                if key.startswith(name + ".") or key == name:
                    enabled_classes.append(cls)
                    matched = True

            if not matched:
                logger.warning(f"No detector found matching '{name}'")

        return enabled_classes

    def get_by_name(self, name: str) -> Optional[Type[BaseDetector]]:
        """Look up a specific detector by its registry key."""
        return self._registry.get(name)

    def get_categories(self) -> List[str]:
        """Return all detector categories (e.g., injection, xss, crypto)."""
        categories = set()
        for key in self._registry:
            parts = key.split(".")
            if len(parts) >= 2:
                categories.add(parts[0])
        return sorted(categories)

    def summary(self) -> Dict[str, int]:
        """Return a count of detectors per category."""
        counts: Dict[str, int] = {}
        for key in self._registry:
            category = key.split(".")[0]
            counts[category] = counts.get(category, 0) + 1
        return counts
