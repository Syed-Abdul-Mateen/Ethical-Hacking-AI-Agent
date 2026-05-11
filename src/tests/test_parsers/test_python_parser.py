"""Tests for the Python parser."""

import pytest
import tempfile
from pathlib import Path

from src.utils.config import Config


@pytest.fixture
def config(tmp_path):
    """Create a minimal config for parser instantiation."""
    config_content = """
agent:
  name: "Test"
parsers: {}
"""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    return Config(config_file)


@pytest.fixture
def sample_python_file(tmp_path):
    """Create a sample Python file for testing."""
    code = '''
import os
import sys
from pathlib import Path

def login(username, password):
    """Login function."""
    query = "SELECT * FROM users WHERE name='" + username + "'"
    cursor.execute(query)
    return True

class UserManager:
    def delete_user(self, user_id):
        eval(user_id)
        pass
'''
    file_path = tmp_path / "sample.py"
    file_path.write_text(code)
    return file_path


class TestPythonParser:
    """Test suite for PythonParser."""

    def test_parse_returns_parsed_file(self, config, sample_python_file):
        """Test that parsing returns a valid ParsedFile."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(sample_python_file)
        assert result is not None
        assert result.language == "python"
        assert result.content is not None

    def test_extracts_imports(self, config, sample_python_file):
        """Test that imports are extracted."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(sample_python_file)
        assert "os" in result.metadata["imports"]
        assert "sys" in result.metadata["imports"]

    def test_extracts_functions(self, config, sample_python_file):
        """Test that function names are extracted."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(sample_python_file)
        assert "login" in result.metadata["functions"]
        assert "delete_user" in result.metadata["functions"]

    def test_extracts_classes(self, config, sample_python_file):
        """Test that class names are extracted."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(sample_python_file)
        assert "UserManager" in result.metadata["classes"]

    def test_detects_dangerous_calls(self, config, sample_python_file):
        """Test that dangerous calls (eval, exec) are detected."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(sample_python_file)
        assert "eval" in result.metadata["dangerous_calls"]

    def test_nonexistent_file_returns_none(self, config):
        """Test that a nonexistent file returns None."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(Path("/nonexistent/file.py"))
        assert result is None

    def test_ast_is_present(self, config, sample_python_file):
        """Test that the AST is present in the parsed result."""
        from src.parsers.python_parser import PythonParser
        parser = PythonParser(config)
        result = parser.parse(sample_python_file)
        assert result.ast is not None
