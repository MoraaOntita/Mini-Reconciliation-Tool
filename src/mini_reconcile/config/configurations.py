"""
------------------------------------------------------------------------------
Configuration Loader Module for Mini Reconciliation Tool

This module provides a reusable class and helper function to load and manage
application configuration from a YAML file. It supports multiple ways to locate
the configuration file:
  1) An explicit file path argument.
  2) An environment variable (RECONCILE_CONFIG_PATH).
  3) A default relative path fallback.

The configuration is expected to define merge keys, suffixes, column mappings,
comparison rules, and result labels used throughout the reconciliation process.

Key Components:
- ConfigLoader: Loads YAML config and exposes it as a Python dictionary.
- load_config: Backward-compatible convenience function to instantiate loader.

This allows the reconciliation logic to remain flexible and environment-agnostic.
------------------------------------------------------------------------------
"""


import yaml
from pathlib import Path
from typing import Any, Dict, Optional
import os


class ConfigLoader:
    """
    Loads reconciliation configuration from a YAML file.
    """

    DEFAULT_CONFIG_FILENAME = "config.yaml"
    ENV_VAR_NAME = "RECONCILE_CONFIG_PATH"

    def __init__(self, path: Optional[str] = None) -> None:
        """
        Initialize ConfigLoader.

        :param path: Optional explicit path to config YAML.
        """
        self.path = self.resolve_config_path(path)

    def resolve_config_path(self, path: Optional[str]) -> Path:
        """
        Resolve the config path in this order:
        1) Explicit path argument
        2) Env var `RECONCILE_CONFIG_PATH`
        3) Default: ../../../config/config.yaml relative to this file
        """
        if path:
            return Path(path).resolve()
        env_path = os.getenv(self.ENV_VAR_NAME)
        if env_path:
            return Path(env_path).resolve()
        # fallback: 3 dirs up from here + /config/config.yaml
        return (Path(__file__).parents[3] / 'config' / self.DEFAULT_CONFIG_FILENAME).resolve()

    def load(self) -> Dict[str, Any]:
        """
        Load the YAML config as a dictionary.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found at {self.path}")
        with self.path.open("r") as f:
            config = yaml.safe_load(f)
        return config


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """
    Backward-compatible helper for legacy usage.
    """
    return ConfigLoader(path).load()
