"""
Integration test for full scan.
"""

import pytest
from pathlib import Path

from src.utils.config import Config


@pytest.fixture
def config(tmp_path):
    """Create a minimal config for integration testing."""
    output_dir = str(tmp_path / "reports").replace("\\", "/")
    config_content = (
        "agent:\n"
        "  name: Integration Test\n"
        "  version: 0.1.0\n"
        "  max_file_size_mb: 10\n"
        "  follow_symlinks: false\n"
        "  max_workers: 2\n"
        "\n"
        "walker:\n"
        "  ignore_patterns:\n"
        "    - __pycache__\n"
        "    - .git\n"
        "\n"
        "parsers:\n"
        "  .php: src.parsers.php_parser.PHPParser\n"
        "  .py: src.parsers.python_parser.PythonParser\n"
        "\n"
        "detectors:\n"
        "  enabled:\n"
        "    - injection.sql_injection\n"
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


def test_full_scan_with_vulnerable_file(config, tmp_path):
    """Integration test: scan a directory with a known vulnerable PHP file."""
    from src.orchestrator.agent import Agent

    # Create a simple vulnerable file
    vuln_file = tmp_path / "test.php"
    vuln_file.write_text("<?php $query = 'SELECT * FROM users WHERE id=' . $_GET['id']; ?>")

    agent = Agent(config)
    summary = agent.run_scan(
        target_path=tmp_path,
        output_dir=tmp_path / "output",
    )

    assert summary is not None
    assert summary["files_scanned"] >= 1
    assert "reports" in summary