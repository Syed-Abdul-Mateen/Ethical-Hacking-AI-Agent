"""Calculate CVSS scores for findings based on severity and context."""

from typing import Optional

from src.detectors.base_detector import Finding


class CVSSCalculator:
    """
    Simple mapping from severity to CVSS v3 base score.
    More advanced scoring would use actual vectors, but for simplicity we approximate.
    """

    SEVERITY_SCORES = {
        "critical": 9.0,
        "high": 7.5,
        "medium": 5.5,
        "low": 3.0,
        "info": 0.0,
    }

    def calculate(self, finding: Finding) -> Optional[float]:
        """
        Calculate CVSS base score for the finding.
        If the finding already has a CVSS score (e.g., from CVE mapping), return that.
        Otherwise, approximate based on severity.
        """
        if finding.cvss_score is not None:
            return finding.cvss_score
        return self.SEVERITY_SCORES.get(finding.severity, 0.0)