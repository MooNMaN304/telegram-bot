"""Standard logger configuration using logging.config.

Uses logging.dictConfig() from the standard library to configure console
and rotating file handlers.
Supports structured JSON logging for centralized log collection with Loki.
"""

import logging
import logging.config
from pathlib import Path
import codecs
import json
import os
from contextvars import ContextVar

# Project root (two levels up from src/services/logger.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_ROOT / "app.log"

# Context variables for service identification
service_name_ctx: ContextVar[str] = ContextVar("service_name", default="unknown")
server_location_ctx: ContextVar[str] = ContextVar("server_location", default="unknown")


class UnicodeDecodeHandler(logging.Handler):
    """Handler that decodes Unicode escape sequences in log messages."""

    def __init__(self, target_handler):
        super().__init__()
        self.target_handler = target_handler

    def emit(self, record):
        """Transform Unicode escapes and pass to target handler."""
        try:
            # Decode Unicode escape sequences in the message
            if isinstance(record.msg, str):
                # Try to parse as JSON first
                try:
                    # If it's JSON, parse and re-serialize with ensure_ascii=False
                    if record.msg.strip().startswith(("{", "[")):
                        parsed = json.loads(record.msg)
                        record.msg = json.dumps(parsed, ensure_ascii=False, indent=2)
                except (json.JSONDecodeError, ValueError):
                    # If not JSON, just decode unicode escapes
                    try:
                        record.msg = codecs.decode(record.msg, "unicode_escape")
                    except Exception:
                        pass

            # Also decode args if they contain Unicode escapes
            if record.args:
                decoded_args = []
                for arg in record.args if isinstance(record.args, tuple) else [record.args]:
                    if isinstance(arg, str):
                        try:
                            if arg.strip().startswith(("{", "[")):
                                parsed = json.loads(arg)
                                decoded_args.append(
                                    json.dumps(parsed, ensure_ascii=False, indent=2)
                                )
                            else:
                                decoded_args.append(codecs.decode(arg, "unicode_escape"))
                        except Exception:
                            decoded_args.append(arg)
                    else:
                        decoded_args.append(arg)
                record.args = (
                    tuple(decoded_args) if isinstance(record.args, tuple) else decoded_args[0]
                )
        except Exception:
            pass  # If decoding fails, use original message

        self.target_handler.emit(record)

    def setFormatter(self, fmt):
        """Pass formatter to target handler."""
        self.target_handler.setFormatter(fmt)


# Standard logging configuration dictionary
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [%(service_name)s@%(server_location)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(service_name)s %(server_location)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json" if os.getenv("LOG_FORMAT", "text").lower() == "json" else "default",
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
    "loggers": {
        # Подавляем шумные логи внешних библиотек
        "telebot": {
            "level": "CRITICAL",
            "propagate": False,
        },
        "telebot.util": {
            "level": "CRITICAL",
            "propagate": False,
        },
        "telebot.apihelper": {
            "level": "CRITICAL",
            "propagate": False,
        },
        "sqlalchemy": {
            "level": "WARNING",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "level": "WARNING",
            "propagate": False,
        },
        "selenium": {
            "level": "WARNING",
            "propagate": False,
        },
        "urllib3": {
            "level": "WARNING",
            "propagate": False,
        },
    },
}


def setup_logging(config: dict = None, service_name: str = None, server_location: str = None) -> None:
    """Configure logging using dictConfig from the standard library.

    Args:
        config: Optional logging configuration dict. If None, uses LOGGING_CONFIG.
        service_name: Name of the service (e.g., 'telegram-bot', 'celery-worker')
        server_location: Server location (e.g., 'frankfurt', 'moscow')
    """
    if config is None:
        config = LOGGING_CONFIG

    # Set context variables if provided
    if service_name:
        service_name_ctx.set(service_name)
    if server_location:
        server_location_ctx.set(server_location)

    # Ensure log file directory exists
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    logging.config.dictConfig(config)

    # Wrap handlers with Unicode decoder
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        unicode_handler = UnicodeDecodeHandler(handler)
        unicode_handler.setLevel(handler.level)
        unicode_handler.setFormatter(handler.formatter)
        root_logger.removeHandler(handler)
        root_logger.addHandler(unicode_handler)


def set_service_context(service_name: str, server_location: str) -> None:
    """Set service name and server location for structured logging.

    Args:
        service_name: Name of the service (e.g., 'telegram-bot', 'celery-worker')
        server_location: Server location (e.g., 'frankfurt', 'moscow')
    """
    service_name_ctx.set(service_name)
    server_location_ctx.set(server_location)


def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance with service context.

    Args:
        name: Logger name (typically __name__). If None, returns root logger.

    Returns:
        logging.Logger instance with added context filter
    """
    logger = logging.getLogger(name)

    # Add filter to inject service context into log records
    class ServiceContextFilter(logging.Filter):
        def filter(self, record):
            record.service_name = service_name_ctx.get()
            record.server_location = server_location_ctx.get()
            return True

    logger.addFilter(ServiceContextFilter())
    return logger


__all__ = ["setup_logging", "get_logger", "set_service_context", "LOGGING_CONFIG"]
