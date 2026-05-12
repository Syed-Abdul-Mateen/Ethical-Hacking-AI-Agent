"""
Test Utilities Package

This module contains shared fixtures, mock objects, and utility functions 
for executing unit and integration tests across the Ethical Hacking AI Agent.
"""

import logging
import pytest

def disable_logging_for_tests():
    """Disable all standard logging during test execution to reduce terminal noise."""
    logging.getLogger().setLevel(logging.CRITICAL)

def mock_vulnerability_finding(rule_id="TEST_001", severity="HIGH", title="Test Vulnerability"):
    """
    Generate a standardized mock finding dictionary for testing reporting and export logic.
    """
    return {
        "rule_id": rule_id,
        "title": title,
        "severity": severity,
        "description": "This is an automated test vulnerability injected via test utilities.",
        "file_path": "tests/mock_target.py",
        "line_number": 42,
        "match": "eval(user_input)",
        "remediation": "Replace with safer alternative or sanitize input."
    }
