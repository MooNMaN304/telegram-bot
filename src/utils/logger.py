"""Standard logger configuration using logging.config.

Uses logging.dictConfig() from the standard library to configure console 
and rotating file handlers.
"""
import logging
import logging.config
from pathlib import Path
import codecs
import json

# Project root (two levels up from src/services/logger.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = PROJECT_ROOT / "app.log"


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
                    if record.msg.strip().startswith(('{', '[')):
                        parsed = json.loads(record.msg)
                        record.msg = json.dumps(parsed, ensure_ascii=False, indent=2)
                except (json.JSONDecodeError, ValueError):
                    # If not JSON, just decode unicode escapes
                    try:
                        record.msg = codecs.decode(record.msg, 'unicode_escape')
                    except Exception:
                        pass
            
            # Also decode args if they contain Unicode escapes
            if record.args:
                decoded_args = []
                for arg in record.args if isinstance(record.args, tuple) else [record.args]:
                    if isinstance(arg, str):
                        try:
                            if arg.strip().startswith(('{', '[')):
                                parsed = json.loads(arg)
                                decoded_args.append(json.dumps(parsed, ensure_ascii=False, indent=2))
                            else:
                                decoded_args.append(codecs.decode(arg, 'unicode_escape'))
                        except Exception:
                            decoded_args.append(arg)
                    else:
                        decoded_args.append(arg)
                record.args = tuple(decoded_args) if isinstance(record.args, tuple) else decoded_args[0]
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
    
    # Wrap handlers with Unicode decoder
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        unicode_handler = UnicodeDecodeHandler(handler)
        unicode_handler.setLevel(handler.level)
        unicode_handler.setFormatter(handler.formatter)
        root_logger.removeHandler(handler)
        root_logger.addHandler(unicode_handler)


def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Logger name (typically __name__). If None, returns root logger.
    
    Returns:
        logging.Logger instance
    """
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger", "LOGGING_CONFIG"]