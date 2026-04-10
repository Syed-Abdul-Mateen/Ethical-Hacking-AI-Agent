# Adding a New Detector

1. Create a new Python file in `src/detectors/` under appropriate category.
2. Inherit from `BaseDetector` and implement `run(scan_context: ScanContext) -> List[Finding]`.
3. Use `scan_context.parsed_files` to access parsed data.
4. Return a list of `Finding` objects.
5. Add the detector to `src/orchestrator/planner.py`'s detector loading logic (or let it be auto-loaded if you use dynamic loading).
6. Update `configs/detectors_config.yaml` to enable/disable the detector.

Example:

```python
from src.detectors.base_detector import BaseDetector, Finding
from src.orchestrator.context import ScanContext

class MyDetector(BaseDetector):
    def run(self, scan_context: ScanContext) -> List[Finding]:
        findings = []
        for parsed in scan_context.parsed_files:
            # Analyze parsed.parsed_data
            finding = Finding(
                title="My Vulnerability",
                description="...",
                file_path=parsed.file_path,
                line_number=42,
                severity="high",
                cvss_score=8.0,
                remediation="...",
                cwe_id="CWE-123"
            )
            findings.append(finding)
        return findings