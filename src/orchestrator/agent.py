"""Main agent class that orchestrates the entire scanning process."""

import signal
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from tqdm import tqdm

from src.orchestrator.context import ScanContext
from src.orchestrator.planner import Planner
from src.orchestrator.registry import DetectorRegistry
from src.orchestrator.ai_analyzer import AIAnalyzer
from src.orchestrator.remediation_engine import RemediationEngine
from src.orchestrator.exceptions import ScanInterrupted, ConfigurationError
from src.file_system.walker import FileWalker
from src.file_system.file_classifier import FileClassifier
from src.reporting.generator import ReportGenerator
from src.utils.logger import get_logger
from src.utils.config import Config
from src.utils.deduplicator import Deduplicator
from src.utils.cvss_calculator import CVSSCalculator

logger = get_logger(__name__)


class Agent:
    """
    Ethical Hacking AI Agent – orchestrates the entire security scan.

    The agent:
    - Loads configuration
    - Walks the target directory
    - Classifies files and runs appropriate parsers
    - Invokes detectors based on the planner
    - Aggregates findings and generates reports
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the agent with optional configuration.

        Args:
            config: Configuration object. If None, loads from default path.
        """
        self.config = config or Config()
        self.context: Optional[ScanContext] = None
        self.planner = Planner(self.config)
        self.file_walker = FileWalker(self.config)
        self.file_classifier = FileClassifier(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.deduplicator = Deduplicator()
        self.cvss_calculator = CVSSCalculator()
        self.ai_analyzer = AIAnalyzer()
        self.remediation_engine = RemediationEngine()

        # Plugin registry for auto-discovering detectors
        self.registry = DetectorRegistry(self.config)

        # Concurrency settings
        self.max_workers = self.config.get("agent.max_workers", 4)

        # Register signal handlers for graceful interruption (Main Thread only)
        import threading
        if threading.current_thread() is threading.main_thread():
            try:
                signal.signal(signal.SIGINT, self._handle_interrupt)
                signal.signal(signal.SIGTERM, self._handle_interrupt)
            except (ValueError, RuntimeError):
                pass

    def _handle_interrupt(self, signum, frame) -> None:
        """Handle Ctrl+C / termination signals."""
        logger.warning("Received interrupt signal. Aborting scan...")
        if self.context:
            self.context.interrupted = True
        sys.exit(1)

    def _update_status(self, phase: str, progress: int, message: str):
        """Write current scan status to a file for the Web UI."""
        if not self.context or not self.context.output_dir:
            return
        status_file = self.context.output_dir / "status.json"
        status_data = {
            "phase": phase,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        try:
            self.context.output_dir.mkdir(parents=True, exist_ok=True)
            with open(status_file, "w") as f:
                json.dump(status_data, f)
        except Exception:
            pass

    def run_scan(
        self,
        target_path: Path,
        output_dir: Optional[Path] = None,
        dynamic: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute a full security scan on the given target.

        Args:
            target_path: Root directory of the website to scan.
            output_dir: Directory where reports will be saved.
            dynamic: Whether to also perform dynamic testing.
            **kwargs: Additional overrides for context.

        Returns:
            Dictionary containing scan summary and path to reports.

        Raises:
            ConfigurationError: If target is invalid or configuration is wrong.
            ScanInterrupted: If the scan was interrupted by the user.
        """
        start_time = datetime.now()
        logger.info(f"Starting scan on target: {target_path}")

        # Validate target
        target_path = Path(target_path).resolve()
        if not target_path.is_dir():
            raise ConfigurationError(f"Target is not a directory: {target_path}")

        # Prepare context
        self.context = ScanContext(
            target_path=target_path,
            config=self.config,
            output_dir=output_dir,
            dynamic_enabled=dynamic,
            **kwargs,
        )

        try:
            # Phase 1: File traversal
            self._update_status("Discovery", 10, "Infiltrating file system...")
            logger.info("Phase 1: Walking file system...")
            all_files = self.file_walker.walk(target_path)
            self.context.files_scanned = all_files
            logger.info(f"Found {len(all_files)} files to analyse.")

            # Phase 2: Classification & parsing (concurrent)
            self._update_status("Parsing", 30, f"Analyzing {len(all_files)} source files...")
            logger.info("Phase 2: Parsing files (concurrent)...")
            parsed_data = self._parse_files_concurrent(all_files)
            self.context.parsed_data = parsed_data

            # Phase 3: Detector planning (using registry)
            self._update_status("Planning", 50, "Orchestrating security modules...")
            logger.info("Phase 3: Planning detectors...")
            detectors_to_run = self.registry.get_enabled()
            if not detectors_to_run:
                # Fallback to planner-based loading
                detectors_to_run = self.planner.plan(self.context)
            logger.info(f"Will run {len(detectors_to_run)} detectors.")

            # Phase 4: Run detectors (concurrent)
            self._update_status("Analysis", 70, "Hunting for vulnerabilities...")
            logger.info("Phase 4: Running detectors (concurrent)...")
            all_findings = self._run_detectors_concurrent(detectors_to_run, parsed_data)

            # Phase 5: Deduplication & CVSS scoring
            self._update_status("Intelligence", 90, "Finalizing threat intelligence...")
            logger.info("Phase 5: Post-processing findings...")
            unique_findings = self.deduplicator.deduplicate(all_findings)
            for finding in unique_findings:
                finding.cvss_score = self.cvss_calculator.calculate(finding)
                
                # AI Enhancement (Advanced Feature)
                if self.config.get("agent.ai_analysis_enabled", True):
                    try:
                        self.ai_analyzer.analyze_finding(finding)
                    except Exception as e:
                        logger.error(f"AI Analysis failed for {finding.title}: {e}")
                    
            self.context.findings = unique_findings

            # Phase 6: Dependency analysis (if enabled)
            if self.config.get("dependency.enabled", True):
                logger.info("Phase 6: Analysing dependencies...")
                try:
                    from src.dependency_analyzer.scanner import DependencyScanner
                    scanner = DependencyScanner(self.config.get("dependency.vuln_db_path"))
                    vuln_deps = scanner.scan_directory(target_path)
                    self.context.vulnerable_dependencies = vuln_deps
                except Exception as e:
                    logger.error(f"Dependency analysis failed: {e}")
                    self.context.add_error("DependencyScanner", str(e))

            # Phase 7: Secrets detection
            secrets_patterns = self.config.get("secrets.patterns_file")
            if secrets_patterns and Path(secrets_patterns).exists():
                logger.info("Phase 7: Detecting secrets...")
                try:
                    from src.secrets_detector.detector import SecretsDetector
                    secrets_detector = SecretsDetector(str(secrets_patterns) if secrets_patterns else None)
                    secrets = []
                    for fp, p_data in parsed_data.items():
                        content = p_data.content if hasattr(p_data, 'content') else ""
                        if content:
                            secrets.extend(secrets_detector.scan(str(content), str(fp)))
                    self.context.secrets_findings = secrets
                except Exception as e:
                    logger.error(f"Secrets detection failed: {e}")
                    self.context.add_error("SecretsDetector", str(e))

            # Phase 8: Dynamic testing (if enabled)
            if dynamic:
                self._update_status("Dynamic Analysis", 95, "Launching active payload injections...")
                logger.info("Phase 8: Running dynamic tests...")
                try:
                    from src.dynamic_tester.scanner import DynamicScanner
                    dynamic_scanner = DynamicScanner(self.config, self.context)
                    dynamic_findings = dynamic_scanner.run(target_url=kwargs.get('original_target'))
                    self.context.dynamic_findings = dynamic_findings
                except Exception as e:
                    logger.error(f"Dynamic testing failed: {e}")
                    self.context.add_error("DynamicScanner", str(e))

            # Phase 9: Merge all findings for reporting
            logger.info("Phase 9: Consolidating all findings...")
            all_combined = list(unique_findings)
            if self.context.dynamic_findings:
                all_combined.extend(self.context.dynamic_findings)
            if self.context.secrets_findings:
                all_combined.extend(self.context.secrets_findings)
            self.context.findings = all_combined

            # Phase 10: Generate reports (including SARIF)
            logger.info("Phase 10: Generating reports...")
            report_paths = self.report_generator.generate(self.context)
            self.context.report_paths = report_paths

            # Count severities across ALL findings
            critical_count = sum(1 for f in all_combined if hasattr(f, 'severity') and f.severity.lower() == 'critical')
            high_count = sum(1 for f in all_combined if hasattr(f, 'severity') and f.severity.lower() == 'high')
            medium_count = sum(1 for f in all_combined if hasattr(f, 'severity') and f.severity.lower() == 'medium')
            low_count = sum(1 for f in all_combined if hasattr(f, 'severity') and f.severity.lower() == 'low')

            # Summary
            elapsed = datetime.now() - start_time
            summary = {
                "target": str(target_path),
                "files_scanned": len(all_files),
                "files_parsed": len(parsed_data),
                "findings_count": len(all_combined),
                "critical_count": critical_count,
                "high_count": high_count,
                "medium_count": medium_count,
                "low_count": low_count,
                "vulnerable_dependencies": len(self.context.vulnerable_dependencies),
                "secrets_found": len(self.context.secrets_findings) if self.context.secrets_findings else 0,
                "dynamic_findings": len(self.context.dynamic_findings) if self.context.dynamic_findings else 0,
                "reports": report_paths,
                "elapsed_seconds": elapsed.total_seconds(),
                "detectors_run": len(detectors_to_run),
                "errors": len(self.context.errors),
            }
            logger.info(f"Scan completed. Summary: {summary}")
            return summary

        except Exception as e:
            logger.exception("Fatal error during scan")
            if output_dir:
                status_file = Path(output_dir) / "status.json"
                self._update_status(status_file, "Failed", 0, f"Error: {str(e)}")
            raise
        finally:
            # Cleanup temporary files
            self._cleanup()

    def _parse_files_concurrent(self, all_files: List[Path]) -> Dict[Path, Any]:
        """Parse files using a thread pool for concurrency."""
        parsed_data = {}

        def _parse_single(file_path: Path):
            parser = self.file_classifier.get_parser(file_path)
            if parser:
                try:
                    parsed = parser.parse(file_path)
                    if parsed:
                        return file_path, parsed
                except Exception as e:
                    logger.error(f"Error parsing {file_path}: {e}", exc_info=True)
                    if self.context:
                        self.context.add_error(str(file_path), str(e))
            return file_path, None

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(_parse_single, fp): fp for fp in all_files}
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Parsing files",
                unit="file",
            ):
                try:
                    file_path, result = future.result()
                    if result:
                        parsed_data[file_path] = result
                except Exception as e:
                    fp = futures[future]
                    logger.error(f"Future error for {fp}: {e}")

        return parsed_data

    def _run_detectors_concurrent(
        self, detector_classes: List, parsed_data: Dict[Path, Any]
    ) -> List:
        """Run detectors concurrently using a thread pool."""
        all_findings = []

        def _run_single(detector_cls):
            try:
                detector = detector_cls(self.config, self.context)
                findings = detector.run(parsed_data)
                return detector_cls.__name__, findings
            except Exception as e:
                logger.error(f"Detector {detector_cls.__name__} failed: {e}", exc_info=True)
                if self.context:
                    self.context.add_error(detector_cls.__name__, str(e))
                return detector_cls.__name__, []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(_run_single, cls): cls for cls in detector_classes}
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Running detectors",
                unit="detector",
            ):
                try:
                    name, findings = future.result()
                    all_findings.extend(findings)
                except Exception as e:
                    cls = futures[future]
                    logger.error(f"Future error for {cls.__name__}: {e}")

        return all_findings

    def _cleanup(self) -> None:
        """Remove temporary files created during scan."""
        if self.context and self.context.temp_dir and self.context.temp_dir.exists():
            import shutil
            try:
                shutil.rmtree(self.context.temp_dir)
                logger.debug(f"Cleaned up temp directory: {self.context.temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean temp dir {self.context.temp_dir}: {e}")