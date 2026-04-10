"""
Test Config loader.
"""

import pytest
from src.utils.config import Config


def test_config_load():
    config = Config()
    assert config.get("agent", "log_level") is not None  # Assuming default