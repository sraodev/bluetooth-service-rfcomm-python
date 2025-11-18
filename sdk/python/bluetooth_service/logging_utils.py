"""Logging helpers for the Bluetooth server SDK."""

from __future__ import annotations

import json
import logging
import logging.config
import os
from pathlib import Path


def configure_logging(
    default_path: str,
    default_level: int = logging.INFO,
    env_key: str | None = "LOG_CFG",
) -> None:
    """
    Configure logging from JSON config or fall back to basic configuration.

    The design follows KISS/BASE by keeping runtime configuration minimal while
    still allowing environment overrides.
    """

    config_path = Path(os.getenv(env_key, default_path) if env_key else default_path)
    if config_path.exists():
        with config_path.open("rt", encoding="utf-8") as config_file:
            config = json.load(config_file)
        logging.config.dictConfig(config)
        return

    logging.basicConfig(level=default_level)

