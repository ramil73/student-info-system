"""Logging setup: writes to both a log file and the console."""
import logging
import os


def setup_logging(log_file: str, level: str = "INFO") -> logging.Logger:
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger("sis")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    if logger.handlers:  # avoid duplicate handlers on repeated calls
        return logger

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    # Console shows only warnings+ so it doesn't clutter the menu
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger
