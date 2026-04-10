"""
Dependency analyzer module.
"""

from src.dependency_analyzer.scanner import DependencyScanner
from src.dependency_analyzer.vuln_db_updater import VulnDBUpdater

__all__ = ["DependencyScanner", "VulnDBUpdater"]