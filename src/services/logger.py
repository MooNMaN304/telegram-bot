"""Standard logger configuration using logging.config.

Uses logging.dictConfig() from the standard library to configure console 
and rotating file handlers.
"""
import logging
import logging.config
from pathlib import Path

# Project root (two levels up from src/services/logger.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_ROOT / "app.log"

# Standard logging configuration dictionary
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": str(LOG_FILE),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}


def setup_logging(config: dict = None) -> None:
    """Configure logging using dictConfig from the standard library.
    
    Args:
        config: Optional logging configuration dict. If None, uses LOGGING_CONFIG.
    """
    if config is None:
        config = LOGGING_CONFIG
    
    # Ensure log file directory exists
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    
    logging.config.dictConfig(config)


def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name (typically __name__). If None, returns root logger.
    
    Returns:
        logging.Logger instance
    """
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger", "LOGGING_CONFIG"]