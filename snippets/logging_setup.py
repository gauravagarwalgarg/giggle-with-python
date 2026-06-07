"""
Logging Setup structured logging with JSON, rotating files, and best practices.

Python's logging module is powerful but poorly documented. This file
gives you production-ready logging configurations you can copy directly.
"""
import json
import logging
import logging.handlers
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# =============================================================================
# BASIC SETUP good enough for scripts
# =============================================================================

def setup_basic_logging(level: str = "INFO"):
    """Quick logging setup for scripts and small apps."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


# =============================================================================
# JSON STRUCTURED LOGGING for production (machine-parseable)
# =============================================================================

class JSONFormatter(logging.Formatter):
    """Format log records as JSON great for log aggregation tools.

    Works with: ELK stack, CloudWatch, Datadog, Splunk, etc.
    """

    def __init__(self, service_name: str = "app", environment: str = "dev"):
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": self.service_name,
            "environment": self.environment,
        }

        # Add source location
        if record.levelno >= logging.WARNING:
            log_data["source"] = {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            }

        # Add exception info
        if record.exc_info and record.exc_info[0]:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Add extra fields (from logger.info("msg", extra={...}))
        extra_keys = set(record.__dict__) - set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)
        for key in extra_keys:
            if not key.startswith("_"):
                log_data[key] = getattr(record, key)

        return json.dumps(log_data, default=str)


# =============================================================================
# ROTATING FILE HANDLER prevent logs from filling disk
# =============================================================================

def setup_production_logging(
    service_name: str = "myapp",
    log_dir: str = "logs",
    level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    json_output: bool = True,
) -> logging.Logger:
    """Production-ready logging with rotation and structured output.

    Creates:
    - Console handler (human-readable)
    - File handler with rotation (JSON for parsing)
    - Error file (only ERROR and above)
    """
    # Create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Root logger configuration
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers.clear()  # Prevent duplicate handlers on re-init

    # Console handler human-readable
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler rotating, JSON formatted
    file_handler = logging.handlers.RotatingFileHandler(
        filename=f"{log_dir}/{service_name}.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    if json_output:
        file_handler.setFormatter(JSONFormatter(service_name=service_name))
    else:
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
        ))
    logger.addHandler(file_handler)

    # Error file only errors and above (easier to monitor)
    error_handler = logging.handlers.RotatingFileHandler(
        filename=f"{log_dir}/{service_name}.error.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter(service_name=service_name))
    logger.addHandler(error_handler)

    return logger


# =============================================================================
# CONTEXT LOGGING add request ID, user info, etc.
# =============================================================================

class ContextFilter(logging.Filter):
    """Add contextual information to every log record.

    Useful for tracing requests through microservices.
    """

    def __init__(self, **defaults):
        super().__init__()
        self.defaults = defaults

    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in self.defaults.items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True


# Thread-local or context-var based request context
import contextvars

_request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")
_user_id: contextvars.ContextVar[str] = contextvars.ContextVar("user_id", default="anonymous")


class RequestContextFilter(logging.Filter):
    """Automatically adds request_id and user_id from context."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id.get()
        record.user_id = _user_id.get()
        return True


def set_request_context(request_id: str, user_id: str = "anonymous"):
    """Set context for the current request (call at request start)."""
    _request_id.set(request_id)
    _user_id.set(user_id)


# =============================================================================
# TIMED LOGGING measure and log execution time
# =============================================================================

import functools
import time


def log_execution_time(logger: logging.Logger = None):
    """Decorator that logs function execution time."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _logger = logger or logging.getLogger(func.__module__)
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                _logger.info(
                    f"{func.__name__} completed in {elapsed:.3f}s",
                    extra={"duration_ms": round(elapsed * 1000, 2)}
                )
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                _logger.error(
                    f"{func.__name__} failed after {elapsed:.3f}s: {e}",
                    exc_info=True,
                    extra={"duration_ms": round(elapsed * 1000, 2)}
                )
                raise
        return wrapper
    return decorator


# =============================================================================
# SUPPRESS NOISY LOGGERS
# =============================================================================

def configure_third_party_loggers():
    """Quiet down noisy third-party libraries."""
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


if __name__ == "__main__":
    print("=" * 60)
    print("Logging Demo")
    print("=" * 60)

    # Setup production logging
    logger = setup_production_logging(
        service_name="demo-app",
        log_dir="/tmp/demo-logs",
        level="DEBUG",
    )

    # Add request context
    logger.addFilter(RequestContextFilter())

    # Simulate logging
    set_request_context("req-abc-123", "user-42")

    logger.debug("Starting application")
    logger.info("Processing request", extra={"endpoint": "/api/users", "method": "GET"})
    logger.warning("Slow query detected", extra={"query_ms": 1500})

    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("Calculation failed", exc_info=True)

    # Timed execution
    @log_execution_time(logger)
    def slow_function():
        time.sleep(0.1)
        return "done"

    slow_function()

    print(f"\nLog files written to /tmp/demo-logs/")
    print("  - demo-app.log (all levels, JSON)")
    print("  - demo-app.error.log (errors only)")
