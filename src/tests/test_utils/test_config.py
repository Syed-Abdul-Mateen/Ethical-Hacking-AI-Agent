"""Tests for the Config class."""

import pytest
import tempfile
import os
from pathlib import Path

from src.utils.config import Config, ConfigError


@pytest.fixture
def sample_config_file(tmp_path):
    """Create a temporary config YAML file."""
    config_content = """
agent:
  name: "Test Agent"
  version: "1.0.0"
  max_file_size_mb: 5
  follow_symlinks: false

walker:
  ignore_patterns:
    - "__pycache__"
    - "node_modules"
    - ".git"
  include_extensions: null

detectors:
  enabled:
    - "injection.sql_injection"
    - "xss.reflected_xss"
  disabled: []

reporting:
  output_dir: "./reports"
  formats:
    - "html"
    - "json"
"""
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(config_content)
    return config_file


class TestConfig:
    """Test suite for Config class."""

    def test_load_config_from_file(self, sample_config_file):
        """Test loading a valid YAML config file."""
        config = Config(sample_config_file)
        assert config.get("agent.name") == "Test Agent"
        assert config.get("agent.version") == "1.0.0"

    def test_dot_notation_access(self, sample_config_file):
        """Test accessing nested keys with dot notation."""
        config = Config(sample_config_file)
        assert config.get("agent.max_file_size_mb") == 5
        assert config.get("agent.follow_symlinks") is False

    def test_default_value_for_missing_key(self, sample_config_file):
        """Test that missing keys return the default value."""
        config = Config(sample_config_file)
        assert config.get("nonexistent.key") is None
        assert config.get("nonexistent.key", "fallback") == "fallback"

    def test_list_config_values(self, sample_config_file):
        """Test accessing list values."""
        config = Config(sample_config_file)
        patterns = config.get("walker.ignore_patterns")
        assert isinstance(patterns, list)
        assert "__pycache__" in patterns
        assert "node_modules" in patterns

    def test_all_config(self, sample_config_file):
        """Test getting the entire config dictionary."""
        config = Config(sample_config_file)
        all_config = config.all()
        assert isinstance(all_config, dict)
        assert "agent" in all_config
        assert "walker" in all_config

    def test_missing_config_file_raises_error(self):
        """Test that a missing config file raises ConfigError."""
        with pytest.raises(ConfigError):
            Config("/nonexistent/path/config.yaml")

    def test_detectors_config(self, sample_config_file):
        """Test reading detectors configuration."""
        config = Config(sample_config_file)
        enabled = config.get("detectors.enabled")
        assert isinstance(enabled, list)
        assert "injection.sql_injection" in enabled

    def test_reporting_formats(self, sample_config_file):
        """Test reading reporting formats."""
        config = Config(sample_config_file)
        formats = config.get("reporting.formats")
        assert "html" in formats
        assert "json" in formats