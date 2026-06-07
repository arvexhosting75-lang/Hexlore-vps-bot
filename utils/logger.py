"""Logging configuration and utilities"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import config

# Color codes for terminal output
class ColorCodes:
    DEBUG = "\033[36m"  # Cyan
    INFO = "\033[32m"  # Green
    WARNING = "\033[33m"  # Yellow
    ERROR = "\033[31m"  # Red
    CRITICAL = "\033[35m"  # Magenta
    RESET = "\033[0m"  # Reset


class ColoredFormatter(logging.Formatter):
    """Colored log formatter"""

    COLORS = {
        logging.DEBUG: ColorCodes.DEBUG,
        logging.INFO: ColorCodes.INFO,
        logging.WARNING: ColorCodes.WARNING,
        logging.ERROR: ColorCodes.ERROR,
        logging.CRITICAL: ColorCodes.CRITICAL,
    }

    def format(self, record):
        levelno = record.levelno
        if levelno in self.COLORS:
            record.levelname = f"{self.COLORS[levelno]}{record.levelname}{ColorCodes.RESET}"
        return super().format(record)


def setup_logging():
    """Setup logging configuration"""
    # Create logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Create formatters
    console_formatter = ColoredFormatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler
    log_file = Path(config.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=config.LOG_FILE_SIZE,
        backupCount=config.LOG_BACKUP_COUNT,
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get logger instance

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
