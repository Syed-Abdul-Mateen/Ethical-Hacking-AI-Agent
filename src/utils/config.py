"""Configuration loader for the agent."""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when configuration loading fails."""
    pass


class Config:
    """Loads and provides access to configuration from YAML files and environment variables."""

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to main agent YAML configuration file.
                         If None, uses AGENT_CONFIG_PATH env var or defaults to
                         './configs/agent_config.yaml'.
        """
        # Load environment variables from .env file if present
        load_dotenv()

        # Determine config path
        if config_path is None:
            config_path = os.getenv("AGENT_CONFIG_PATH", "./configs/agent_config.yaml")
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise ConfigError(f"Configuration file not found: {self.config_path}")

        # Load YAML
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        # Allow environment variable overrides (e.g., AGENT__WALKER__IGNORE_PATTERNS)
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        """
        Override config values with environment variables.
        Env var format: SECTION__KEY (double underscore) for nested keys.
        Example: AGENT__WALKER__IGNORE_PATTERNS would override agent.walker.ignore_patterns.
        """
        prefix = "AGENT__"
        for env_key, env_value in os.environ.items():
            if not env_key.startswith(prefix):
                continue
            # Remove prefix and split by __
            path = env_key[len(prefix):].lower().split("__")
            target = self._config
            for part in path[:-1]:
                if part not in target:
                    target[part] = {}
                target = target[part]
            # Convert env_value to appropriate type (bool, int, float, list)
            last_key = path[-1]
            if env_value.lower() in ("true", "false"):
                target[last_key] = env_value.lower() == "true"
            elif env_value.isdigit():
                target[last_key] = int(env_value)
            else:
                try:
                    target[last_key] = float(env_value)
                except ValueError:
                    # If it's a comma-separated list
                    if "," in env_value:
                        target[last_key] = [x.strip() for x in env_value.split(",")]
                    else:
                        target[last_key] = env_value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-separated key.

        Args:
            key: e.g., "agent.walker.ignore_patterns"
            default: Value to return if key not found.

        Returns:
            Configuration value or default.
        """
        parts = key.split(".")
        value = self._config
        try:
            for part in parts:
                value = value[part]
            return value
        except (KeyError, TypeError):
            return default

    def all(self) -> Dict[str, Any]:
        """Return the entire configuration dictionary."""
        return self._config.copy()