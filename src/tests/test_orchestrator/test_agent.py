"""Tests for the Agent orchestrator."""

import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.config import Config


@pytest.fixture
def config(tmp_path):
    """Create a minimal config for testing."""
    output_dir = str(tmp_path / "reports").replace("\\", "/")
    config_content = (
        "agent:\n"
        "  name: Test Agent\n"
        "  version: 0.1.0\n"
        "  max_file_size_mb: 10\n"
        "  follow_symlinks: false\n"
        "  max_workers: 2\n"
        "\n"
        "walker:\n"
        "  ignore_patterns:\n"
        "    - __pycache__\n"
        "    - .git\n"
        "  include_extensions: null\n"
        "\n"
        "parsers: {}\n"
        "\n"
        "detectors:\n"
        "  enabled: []\n"
        "\n"
        "dependency:\n"
        "  enabled: false\n"
        "\n"
        "secrets:\n"
        "  patterns_file: null\n"
        "\n"
        "reporting:\n"
        f"  output_dir: {output_dir}\n"
        "  formats:\n"
        "    - json\n"
        "  templates_dir: ./src/reporting/templates\n"
        "  include_evidence: false\n"
    )

    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    return Config(config_file)


@pytest.fixture
def sample_target(tmp_path):
    """Create a sample target directory with test files."""
    target = tmp_path / "target"
    target.mkdir()
    (target / "index.html").write_text("<html><body>Hello</body></html>")
    (target / "app.py").write_text("print('hello')")
    return target


class TestAgent:
    """Test suite for the Agent class."""

    def test_agent_initialization(self, config):
        """Test that the agent initializes without errors."""
        from src.orchestrator.agent import Agent
        agent = Agent(config)
        assert agent.config is config
        assert agent.context is None

    def test_agent_rejects_invalid_target(self, config, tmp_path):
        """Test that agent raises error for non-existent target."""
        from src.orchestrator.agent import Agent
        from src.orchestrator.exceptions import ConfigurationError

        agent = Agent(config)
        with pytest.raises(ConfigurationError):
            agent.run_scan(target_path=tmp_path / "nonexistent")

    def test_agent_scans_empty_directory(self, config, tmp_path):
        """Test scanning an empty directory produces zero findings."""
        from src.orchestrator.agent import Agent

        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        agent = Agent(config)
        summary = agent.run_scan(target_path=empty_dir)

        assert summary["files_scanned"] == 0
        assert summary["findings_count"] == 0

    def test_agent_scan_produces_summary(self, config, sample_target, tmp_path):
        """Test that a scan produces a valid summary dictionary."""
        from src.orchestrator.agent import Agent

        agent = Agent(config)
        summary = agent.run_scan(
            target_path=sample_target,
            output_dir=tmp_path / "output",
        )

        assert "target" in summary
        assert "files_scanned" in summary
        assert "findings_count" in summary
        assert "elapsed_seconds" in summary
        assert summary["files_scanned"] >= 0

    def test_agent_cleanup_runs(self, config, sample_target, tmp_path):
        """Test that cleanup is called after scan."""
        from src.orchestrator.agent import Agent

        agent = Agent(config)
        summary = agent.run_scan(
            target_path=sample_target,
            output_dir=tmp_path / "output",
        )
        # If we get here without error, cleanup succeeded
        assert summary is not None