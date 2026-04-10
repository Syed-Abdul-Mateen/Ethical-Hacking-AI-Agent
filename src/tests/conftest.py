"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path


@pytest.fixture
def sample_files_dir():
    """Return path to sample files directory."""
    return Path(__file__).parent / "sample_files"