"""
Logging utilities for the summarizer package.
"""

import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a logger configured with the specified name and level.

    Args:
        name: The name of the logger
        level: The logging level

    Returns:
        A configured logger
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.setLevel(level)
        logger.propagate = False

    return logger
