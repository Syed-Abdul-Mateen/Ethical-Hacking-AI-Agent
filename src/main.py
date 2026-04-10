#!/usr/bin/env python3
"""Main entry point for the Ethical Hacking AI Agent."""

import sys
import argparse
from pathlib import Path
from typing import Optional

from src.orchestrator.agent import Agent
from src.utils.logger import setup_logging, get_logger
from src.utils.config import Config
from src.orchestrator.exceptions import ConfigurationError

logger = get_logger(__name__)


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Ethical Hacking AI Agent – automated security testing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic static analysis on a folder
  %(prog)s --target /path/to/website

  # Include dynamic testing (starts local server)
  %(prog)s --target /path/to/website --dynamic

  # Specify output directory for reports
  %(prog)s --target /path/to/website --output-dir ./my_reports

  # Use a custom config file
  %(prog)s --target /path/to/website --config ./my_config.yaml
        """
    )

    parser.add_argument(
        "-t", "--target",
        required=True,
        type=Path,
        help="Root folder of the website to scan"
    )

    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        help="Directory to save reports (default: configured output_dir/scan_timestamp)"
    )

    parser.add_argument(
        "-d", "--dynamic",
        action="store_true",
        help="Enable dynamic testing (starts local server and runs live tests)"
    )

    parser.add_argument(
        "-c", "--config",
        type=Path,
        help="Path to configuration file (default: ./configs/agent_config.yaml)"
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging level (default: INFO)"
    )

    parser.add_argument(
        "--log-format",
        default="text",
        choices=["text", "json"],
        help="Log output format (default: text)"
    )

    parser.add_argument(
        "--log-dir",
        type=Path,
        help="Directory to write log files (default: ./data/logs)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Ethical Hacking AI Agent 0.1.0"
    )

    return parser.parse_args(args)


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Setup logging
    setup_logging(
        config_path=None,
        log_level=args.log_level,
        log_format=args.log_format,
        log_dir=args.log_dir or Path("./data/logs")
    )

    try:
        # Load configuration
        config = Config(args.config)

        # Override config with command line if needed
        if args.dynamic:
            # Enable dynamic testing if specified
            config._config.setdefault("dynamic", {})["enabled"] = True

        # Create and run agent
        agent = Agent(config)
        summary = agent.run_scan(
            target_path=args.target,
            output_dir=args.output_dir,
            dynamic=args.dynamic
        )

        # Print summary to console
        print("\n" + "=" * 60)
        print("SCAN COMPLETED")
        print("=" * 60)
        print(f"Target:          {summary['target']}")
        print(f"Files scanned:   {summary['files_scanned']}")
        print(f"Findings:        {summary['findings_count']}")
        print(f"Vulnerable deps: {summary['vulnerable_dependencies']}")
        print(f"Secrets found:   {summary['secrets_found']}")
        if summary.get('dynamic_findings'):
            print(f"Dynamic findings: {summary['dynamic_findings']}")
        print(f"Elapsed:         {summary['elapsed_seconds']:.2f} seconds")
        print("\nReports generated:")
        for fmt, path in summary['reports'].items():
            print(f"  {fmt.upper()}: {path}")
        print("=" * 60)

        return 0

    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
        return 130
    except Exception as e:
        logger.exception("Unexpected error")
        return 1


def cli() -> None:
    """Entry point for console script."""
    sys.exit(main())


if __name__ == "__main__":
    sys.exit(main())