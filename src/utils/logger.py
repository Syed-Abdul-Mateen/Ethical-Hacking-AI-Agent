"""Centralised logging configuration for the agent."""

import logging
import logging.config
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import yaml


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra"):
            log_record.update(record.extra)
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging(
    config_path: Optional[Path] = None,
    log_level: Optional[str] = None,
    log_format: str = "text",
    log_dir: Optional[Path] = None,
) -> None:
    """
    Configure logging for the application.

    Args:
        config_path: Path to logging configuration file (YAML or dictConfig format).
        log_level: Override log level (DEBUG, INFO, WARNING, ERROR).
        log_format: 'text' or 'json'.
        log_dir: Directory to write log files (if None, logs go to console only).
    """
    if config_path and config_path.exists():
        with open(config_path, "r") as f:
            if config_path.suffix in (".yaml", ".yml"):
                config = yaml.safe_load(f)
            else:
                # Assume JSON or Python dict
                import json
                config = json.load(f)
        logging.config.dictConfig(config)
    else:
        # Basic configuration
        handlers = []
        if log_dir:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"agent_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            handlers.append(file_handler)
            
        console_handler = logging.StreamHandler()
        handlers.append(console_handler)

        # Set formatter
        if log_format == "json":
            formatter = JsonFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        for handler in handlers:
            handler.setFormatter(formatter)

        # Determine log level
        level = getattr(logging, (log_level or "INFO").upper(), logging.INFO)

        # Apply configuration to root logger
        logging.basicConfig(level=level, handlers=handlers)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Usually __name__ of the calling module.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)