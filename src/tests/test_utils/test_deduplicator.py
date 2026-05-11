"""Tests for the Deduplicator class."""

import pytest
from pathlib import Path

from src.utils.deduplicator import Deduplicator
from src.detectors.base_detector import Finding


@pytest.fixture
def deduplicator():
    return Deduplicator()


@pytest.fixture
def sample_findings():
    """Create a list of findings with some duplicates."""
    return [
        Finding(
            title="SQL Injection",
            description="Found SQLi",
            severity="high",
            file_path=Path("/app/login.php"),
            line_start=10,
        ),
        Finding(
            title="SQL Injection",
            description="Found SQLi (duplicate)",
            severity="high",
            file_path=Path("/app/login.php"),
            line_start=10,
        ),
        Finding(
            title="SQL Injection",
            description="Different location",
            severity="high",
            file_path=Path("/app/login.php"),
            line_start=20,
        ),
        Finding(
            title="XSS",
            description="Found XSS",
            severity="medium",
            file_path=Path("/app/search.php"),
            line_start=5,
        ),
    ]


class TestDeduplicator:
    """Test suite for Deduplicator class."""

    def test_removes_duplicates(self, deduplicator, sample_findings):
        """Test that duplicate findings are removed."""
        unique = deduplicator.deduplicate(sample_findings)
        assert len(unique) == 3  # 4 findings - 1 duplicate = 3

    def test_preserves_unique_findings(self, deduplicator, sample_findings):
        """Test that unique findings are preserved."""
        unique = deduplicator.deduplicate(sample_findings)
        titles = [f.title for f in unique]
        assert "SQL Injection" in titles
        assert "XSS" in titles

    def test_empty_list(self, deduplicator):
        """Test deduplication of empty list."""
        assert deduplicator.deduplicate([]) == []

    def test_single_finding(self, deduplicator):
        """Test deduplication of a single finding."""
        finding = Finding(
            title="Test", description="desc", severity="low",
            file_path=Path("/test.py"), line_start=1,
        )
        result = deduplicator.deduplicate([finding])
        assert len(result) == 1
        assert result[0] is finding

    def test_different_files_not_deduplicated(self, deduplicator):
        """Test that same title in different files are not deduplicated."""
        findings = [
            Finding(
                title="SQL Injection", description="desc", severity="high",
                file_path=Path("/app/a.php"), line_start=10,
            ),
            Finding(
                title="SQL Injection", description="desc", severity="high",
                file_path=Path("/app/b.php"), line_start=10,
            ),
        ]
        unique = deduplicator.deduplicate(findings)
        assert len(unique) == 2
