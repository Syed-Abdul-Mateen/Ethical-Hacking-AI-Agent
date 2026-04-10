"""
Secrets detector module.
"""

from src.secrets_detector.detector import SecretsDetector
from src.secrets_detector.high_entropy import HighEntropyDetector

__all__ = ["SecretsDetector", "HighEntropyDetector"]