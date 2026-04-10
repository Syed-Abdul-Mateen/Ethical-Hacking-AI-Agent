"""Main agent class that orchestrates the entire scanning process."""

import signal
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from tqdm import tqdm

from src.orchestrator.context import ScanContext
from src.orchestrator.planner import Planner
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

        # Register signal handlers for graceful interruption
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame) -> None:
        """Handle Ctrl+C / termination signals."""
        logger.warning("Received interrupt signal. Aborting scan...")
        if self.context:
            self.context.interrupted = True
        sys.exit(1)

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
            logger.info("Phase 1: Walking file system...")
            all_files = self.file_walker.walk(target_path)
            self.context.files_scanned = all_files
            logger.info(f"Found {len(all_files)} files to analyse.")

            # Phase 2: Classification & parsing
            logger.info("Phase 2: Parsing files...")
            parsed_data = {}
            for file_path in tqdm(all_files, desc="Parsing files", unit="file"):
                parser = self.file_classifier.get_parser(file_path)
                if parser:
                    try:
                        parsed = parser.parse(file_path)
                        if parsed:
                            parsed_data[file_path] = parsed
                    except Exception as e:
                        logger.error(f"Error parsing {file_path}: {e}", exc_info=True)
                        self.context.add_error(file_path, str(e))
                else:
                    logger.debug(f"No parser for {file_path}, skipping.")
            self.context.parsed_data = parsed_data

            # Phase 3: Detector planning
            logger.info("Phase 3: Planning detectors...")
            detectors_to_run = self.planner.plan(self.context)
            logger.info(f"Will run {len(detectors_to_run)} detectors.")

            # Phase 4: Run detectors
            logger.info("Phase 4: Running detectors...")
            all_findings = []
            for detector_cls in tqdm(detectors_to_run, desc="Running detectors", unit="detector"):
                try:
                    detector = detector_cls(self.config, self.context)
                    findings = detector.run(parsed_data)
                    all_findings.extend(findings)
                except Exception as e:
                    logger.error(f"Detector {detector_cls.__name__} failed: {e}", exc_info=True)
                    self.context.add_error(detector_cls.__name__, str(e))

            # Phase 5: Deduplication & CVSS scoring
            logger.info("Phase 5: Post-processing findings...")
            unique_findings = self.deduplicator.deduplicate(all_findings)
            for finding in unique_findings:
                finding.cvss_score = self.cvss_calculator.calculate(finding)
            self.context.findings = unique_findings

            # Phase 6: Dependency analysis (if enabled)
            if self.config.get("dependency.enabled", True):
                logger.info("Phase 6: Analysing dependencies...")
                from src.dependency_analyzer.scanner import DependencyScanner
                scanner = DependencyScanner(self.config.get("dependency.vuln_db_path"))
                vuln_deps = scanner.scan_directory(target_path)
                self.context.vulnerable_dependencies = vuln_deps

            # Phase 7: Secrets detection (optional, but we'll run if patterns file exists)
            secrets_patterns = self.config.get("secrets.patterns_file")
            if secrets_patterns and Path(secrets_patterns).exists():
                logger.info("Phase 7: Detecting secrets...")
                from src.secrets_detector.detector import SecretsDetector
                secrets_detector = SecretsDetector(str(secrets_patterns) if secrets_patterns else None)
                secrets = []
                for fp, p_data in parsed_data.items():
                    content = p_data.get("raw_content") or p_data.get("content", "")
                    if content:
                        secrets.extend(secrets_detector.scan(str(content), str(fp)))
                self.context.secrets_findings = secrets

            # Phase 8: Dynamic testing (if enabled)
            if dynamic:
                logger.info("Phase 8: Running dynamic tests...")
                from src.dynamic_tester.scanner import DynamicScanner
                dynamic_scanner = DynamicScanner(self.config, self.context)
                dynamic_findings = dynamic_scanner.run()
                self.context.dynamic_findings = dynamic_findings

            # Phase 9: Generate reports
            logger.info("Phase 9: Generating reports...")
            report_paths = self.report_generator.generate(self.context)
            self.context.report_paths = report_paths

            # Summary
            elapsed = datetime.now() - start_time
            summary = {
                "target": str(target_path),
                "files_scanned": len(all_files),
                "files_parsed": len(parsed_data),
                "findings_count": len(unique_findings),
                "vulnerable_dependencies": len(self.context.vulnerable_dependencies),
                "secrets_found": len(self.context.secrets_findings) if self.context.secrets_findings else 0,
                "dynamic_findings": len(self.context.dynamic_findings) if self.context.dynamic_findings else 0,
                "reports": report_paths,
                "elapsed_seconds": elapsed.total_seconds(),
            }
            logger.info(f"Scan completed. Summary: {summary}")
            return summary

        except Exception as e:
            logger.exception("Fatal error during scan")
            raise
        finally:
            # Cleanup temporary files
            self._cleanup()

    def _cleanup(self) -> None:
        """Remove temporary files created during scan."""
        if self.context and self.context.temp_dir and self.context.temp_dir.exists():
            import shutil
            try:
                shutil.rmtree(self.context.temp_dir)
                logger.debug(f"Cleaned up temp directory: {self.context.temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean temp dir {self.context.temp_dir}: {e}")