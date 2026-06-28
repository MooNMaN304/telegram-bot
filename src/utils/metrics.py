"""Prometheus metrics for Telegram Bot monitoring.

Все метрики централизованно объявлены здесь, чтобы:
1. Не плодить дубликаты в разных модулях
2. Иметь единую точку импорта
3. Гарантировать регистрацию метрик до их использования

Использование в коде:
    from src.utils.metrics import (
        bot_requests, parsing_tasks, captcha_detections,
        driver_operations, sessions_found, movies_found,
        connection_checks, bot_errors, parsing_duration,
    )
    bot_requests.labels(handler="start").inc()
"""

import os
from prometheus_client import Counter, Gauge, Histogram, Info


# ============================================================
# Информация о сервисе (статическая метка)
# ============================================================
service_info = Info(
    name="service_info",
    documentation="Static info about the service (name, server location)",
)
service_info.info({
    "service": os.getenv("SERVICE_NAME", "unknown"),
    "server": os.getenv("SERVER_LOCATION", "unknown"),
})


# ============================================================
# Bot handlers
# ============================================================
bot_requests = Counter(
    name="bot_requests_total",
    documentation="Total bot requests by handler name",
    labelnames=["handler"],
)

bot_errors = Counter(
    name="bot_errors_total",
    documentation="Bot errors by error type",
    labelnames=["error_type"],
)


# ============================================================
# Parsing tasks (Celery)
# ============================================================
parsing_tasks = Counter(
    name="parsing_tasks_total",
    documentation="Parsing tasks by parser and status",
    labelnames=["parser", "status"],  # parser: kinomax|malibu, status: success|failed
)

parsing_duration = Histogram(
    name="parsing_duration_seconds",
    documentation="Parsing task duration in seconds",
    labelnames=["parser"],
    buckets=(30, 60, 120, 180, 300, 600, 900, 1200, float("inf")),
)

parsing_in_progress = Gauge(
    name="parsing_in_progress",
    documentation="Currently running parsing tasks (1 = running, 0 = idle)",
    labelnames=["parser"],
)


# ============================================================
# Browser / Driver
# ============================================================
browser_connections = Counter(
    name="browser_connections_total",
    documentation="Browserless connection attempts",
    labelnames=["status"],  # status: success|failed
)

driver_operations = Counter(
    name="driver_operations_total",
    documentation="Selenium driver operations",
    labelnames=["operation"],  # operation: create|close|restart|error
)

captcha_detections = Counter(
    name="captcha_detections_total",
    documentation="Captcha detections on Kinomax",
)


# ============================================================
# Parsing results
# ============================================================
movies_found = Counter(
    name="movies_found_total",
    documentation="Movies found by parser and cinema",
    labelnames=["cinema"],  # cinema: kinomax|malibu
)

sessions_found = Counter(
    name="sessions_found_total",
    documentation="Sessions parsed and saved by cinema",
    labelnames=["cinema"],  # cinema: kinomax|malibu
)

parser_items_skipped = Counter(
    name="parser_items_skipped_total",
    documentation="Movies skipped during parsing",
    labelnames=["cinema"],  # cinema: kinomax|malibu
)


# ============================================================
# Connection checks (Celery)
# ============================================================
connection_checks = Counter(
    name="connection_checks_total",
    documentation="Connection checks to external services",
    labelnames=["resource", "status"],  # resource: redis|db|browserless, status: success|failed
)

# Текущий статус подключений (1 = healthy, 0 = unhealthy)
connection_status = Gauge(
    name="connection_status",
    documentation="Current connection health status by resource",
    labelnames=["resource"],
)


# ============================================================
# Celery worker health
# ============================================================
worker_alive = Gauge(
    name="worker_alive",
    documentation="Worker heartbeat (updated every time a task runs)",
    labelnames=["server_location"],
)


# ============================================================
# Database operations
# ============================================================
db_operations = Counter(
    name="db_operations_total",
    documentation="Database operations by type",
    labelnames=["operation"],  # operation: get_or_create|update|delete
)


__all__ = [
    "service_info",
    "bot_requests",
    "bot_errors",
    "parsing_tasks",
    "parsing_duration",
    "parsing_in_progress",
    "browser_connections",
    "driver_operations",
    "captcha_detections",
    "movies_found",
    "sessions_found",
    "parser_items_skipped",
    "connection_checks",
    "connection_status",
    "worker_alive",
    "db_operations",
]
