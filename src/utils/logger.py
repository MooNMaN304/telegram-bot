"""Standard logger configuration using logging.config.

Uses logging.dictConfig() from the standard library to configure console
and rotating file handlers.
Supports structured JSON logging for centralized log collection with Loki.
"""

import logging
import logging.config
from pathlib import Path
import json
import os
from contextvars import ContextVar

# Project root (two levels up from src/services/logger.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_ROOT / "app.log"

# Context variables for service identification
service_name_ctx: ContextVar[str] = ContextVar("service_name", default="unknown")
server_location_ctx: ContextVar[str] = ContextVar("server_location", default="unknown")


class ServiceContextFilter(logging.Filter):
    """Filter that injects service_name and server_location into log records."""

    def filter(self, record):
        record.service_name = service_name_ctx.get()
        record.server_location = server_location_ctx.get()
        return True


class SafeUnicodeDecodeHandler(logging.Handler):
    """Handler that safely passes records to the target handler.

    Previously, UnicodeDecodeHandler tried to decode messages with
    codecs.decode(msg, 'unicode_escape') which BROKE Russian text
    and also did not wrap target_handler.emit() in try/except,
    causing all logs to be lost when the formatter raised an error.
    
    This new handler only ensures the target handler never crashes the process.
    """

    def __init__(self, target_handler):
        super().__init__()
        self.target_handler = target_handler

    def emit(self, record):
        """Pass record to target handler, never crash.

        IMPORTANT: We must run target handler's filters BEFORE emit(),
        because emit() bypasses filters. Without this, attributes added
        by filters (like service_name, server_location) are missing
        from the record, causing formatter crashes.
        """
        try:
            # Run target handler's filters first
            for f in self.target_handler.filters:
                if not f.filter(record):
                    return
            self.target_handler.emit(record)
        except Exception:
            # Last resort: write to stderr so logs are never silently lost
            try:
                import sys
                msg = f"[LOGGING ERROR] Failed to emit record: {record.getMessage()}\n"
                sys.stderr.write(msg)
                sys.stderr.flush()
            except Exception:
                pass

    def setFormatter(self, fmt):
        """Pass formatter to target handler."""
        self.target_handler.setFormatter(fmt)

    def setLevel(self, level):
        """Pass level to target handler."""
        self.target_handler.setLevel(level)


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
            "format": "%(asctime)s %(levelname)s %(name)s %(service_name)s %(server_location)s %(message)s",
        },
    },
    "filters": {
        "service_context": {
            "()": "src.utils.logger.ServiceContextFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "json" if os.getenv("LOG_FORMAT", "text").lower() == "json" else "default",
            "stream": "ext://sys.stdout",
            "filters": ["service_context"],
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": str(LOG_FILE),
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8",
            "filters": ["service_context"],
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
    "loggers": {
        # Celery internal loggers — добавляем service_context filter
        # чтобы service_name/server_location были не null
        "celery": {
            "level": "INFO",
            "propagate": True,
            "filters": ["service_context"],
        },
        "celery.redirected": {
            "level": "INFO",
            "propagate": True,
            "filters": ["service_context"],
        },
        "celery.worker": {
            "level": "INFO",
            "propagate": True,
            "filters": ["service_context"],
        },
        "celery.worker.strategy": {
            "level": "INFO",
            "propagate": True,
            "filters": ["service_context"],
        },
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

    # Wrap handlers with safe handler that never crashes
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        safe_handler = SafeUnicodeDecodeHandler(handler)
        safe_handler.setLevel(handler.level)
        safe_handler.setFormatter(handler.formatter)
        root_logger.removeHandler(handler)
        root_logger.addHandler(safe_handler)

    logger = get_logger(__name__)
    logger.info(
        "Logging configured: service=%s location=%s format=%s",
        service_name or "unknown",
        server_location or "unknown",
        os.getenv("LOG_FORMAT", "text"),
    )


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

    # Add filter to inject service context into log records.
    # The filter is idempotent — adding it multiple times is safe.
    has_filter = any(
        isinstance(f, ServiceContextFilter) for f in logger.filters
    )
    if not has_filter:
        logger.addFilter(ServiceContextFilter())

    return logger


__all__ = ["setup_logging", "get_logger", "set_service_context", "LOGGING_CONFIG"]
