"""
Integration test for full scan.
"""

import pytest
from src.orchestrator.agent import Agent
from pathlib import Path


def test_full_scan(tmp_path):
    # Create a simple vulnerable file
    vuln_file = tmp_path / "test.php"
    vuln_file.write_text("<?php $query = 'SELECT * FROM users WHERE id=' . $_GET['id']; ?>")
    agent = Agent()
    agent.scan(str(tmp_path))
    assert len(agent.context.findings) > 0