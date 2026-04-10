"""
Package parsers for various ecosystems.
"""

from src.dependency_analyzer.package_parsers.npm_parser import NPMParser
from src.dependency_analyzer.package_parsers.pip_parser import PipParser
from src.dependency_analyzer.package_parsers.composer_parser import ComposerParser
from src.dependency_analyzer.package_parsers.gem_parser import GemParser
from src.dependency_analyzer.package_parsers.maven_parser import MavenParser

__all__ = ["NPMParser", "PipParser", "ComposerParser", "GemParser", "MavenParser"]