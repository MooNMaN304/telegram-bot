"""Celery configuration and tasks for movie parsers.

This module is imported both by:
1. The bot (via admin_commands.py) — should NOT call setup_logging()
2. The celery worker (via celery command) — SHOULD call setup_logging()
"""
import time
import os
import sys
import threading
from celery import Celery, shared_task

from prometheus_client import start_http_server

from src.application.value import get_malibu_controller, build_kinomax_controller
from src.settings import settings
from src.utils.logger import setup_logging, get_logger, set_service_context
from src.utils.metrics import (
    parsing_tasks, parsing_duration, parsing_in_progress,
    browser_connections, connection_checks, connection_status,
    worker_alive, driver_operations,
)

# Определяем, запущены ли мы как celery worker или как бот
_is_celery_worker = 'worker' in sys.argv or os.getenv('CELERY_WORKER_MODE', '') == '1'

if _is_celery_worker:
    # Настройка логирования ТОЛЬКО для Celery worker
    _service_name = os.getenv("SERVICE_NAME", "celery-worker")
    _server_location = os.getenv("SERVER_LOCATION", "unknown")
    setup_logging(service_name=_service_name, server_location=_server_location)
    set_service_context(_service_name, _server_location)

logger = get_logger(__name__)

# service_name / server_location для use в celery_configure()
_service_name = os.getenv("SERVICE_NAME", "celery-worker")
_server_location = os.getenv("SERVER_LOCATION", "unknown")
_metrics_port = int(os.getenv("METRICS_PORT", "8001"))


celery_app = Celery(
    "parsers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

def check_connections():
    """Проверка подключений к БД и Redis перед запуском задач."""
    import socket
    from urllib.parse import urlparse
    
    # Проверка Redis (Broker)
    try:
        url = urlparse(settings.CELERY_BROKER_URL)
        host = url.hostname
        port = url.port or 6379
        logger.info("Проверка подключения к Redis: %s:%s", host, port)
        with socket.create_connection((host, port), timeout=5):
            logger.info("✅ Подключение к Redis успешно")
            connection_checks.labels(resource="redis", status="success").inc()
            connection_status.labels(resource="redis").set(1)
    except Exception as e:
        logger.error("❌ Ошибка подключения к Redis: %s", e)
        connection_checks.labels(resource="redis", status="failed").inc()
        connection_status.labels(resource="redis").set(0)

    # Проверка БД
    try:
        db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "http://")
        url = urlparse(db_url)
        host = url.hostname
        port = url.port or 5432
        logger.info("Проверка подключения к БД: %s:%s", host, port)
        with socket.create_connection((host, port), timeout=5):
            logger.info("✅ Подключение к БД успешно")
            connection_checks.labels(resource="db", status="success").inc()
            connection_status.labels(resource="db").set(1)
    except Exception as e:
        logger.error("❌ Ошибка подключения к БД: %s", e)
        connection_checks.labels(resource="db", status="failed").inc()
        connection_status.labels(resource="db").set(0)

    # Проверка Browserless
    try:
        from urllib.parse import urlparse as _urlparse
        sel_url = _urlparse(settings.REMOTE_SELENIUM_URL)
        host = sel_url.hostname
        port = sel_url.port or 3000
        logger.info("Проверка подключения к Browserless: %s:%s", host, port)
        with socket.create_connection((host, port), timeout=5):
            logger.info("✅ Подключение к Browserless успешно")
            browser_connections.labels(status="success").inc()
            connection_checks.labels(resource="browserless", status="success").inc()
            connection_status.labels(resource="browserless").set(1)
    except Exception as e:
        logger.error("❌ Ошибка подключения к Browserless: %s", e)
        browser_connections.labels(status="failed").inc()
        connection_checks.labels(resource="browserless", status="failed").inc()
        connection_status.labels(resource="browserless").set(0)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
    worker_hijack_root_logger=False,
    # Redis retry policy for connection issues
    broker_transport_options={
        'visibility_timeout': 3600,  # 1 hour
        'fanout_prefix': True,
        'fanout_patterns': True,
    },
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=10,
    broker_connection_timeout=30,
    result_backend_transport_options={
        'retry_policy': {
            'timeout': 30,
        }
    },
)

def celery_configure():
    logger.info("Celery worker configured on %s", _server_location)

    # Запускаем metrics HTTP server
    try:
        start_http_server(_metrics_port)
        logger.info("Prometheus metrics server started on port %d", _metrics_port)
    except Exception as e:
        logger.error("Failed to start metrics server on port %d: %s", _metrics_port, e)

    check_connections()


def _resolve_gigachat_credentials() -> str:
    key = settings.GIGACHAT_API_KEY
    if key.endswith("=="):
        return key
    return key

def _emit_parsing_metrics(parser_name: str, result: dict, task_start: float):
    """Обновляет Prometheus метрики по результатам парсинга."""
    status = result.get("status", "unknown")
    elapsed = result.get("elapsed_seconds", time.time() - task_start)

    parsing_tasks.labels(parser=parser_name, status=status).inc()
    parsing_duration.labels(parser=parser_name).observe(elapsed)
    parsing_in_progress.labels(parser=parser_name).set(0)

    # Heartbeat — воркер жив
    worker_alive.labels(server_location=_server_location).set_to_current_time()


@shared_task(name="parsers.run_kinomax")
def run_kinomax_parser_task(city: str = "Липецк"):
    task_start = time.time()
    controller = None
    parsing_in_progress.labels(parser="kinomax").set(1)
    try:
        logger.info("🎬 [KINOMAX] Задача начата. Город: %s", city)

        step_start = time.time()
        logger.info("🎬 [KINOMAX] Создание контроллера...")
        controller = build_kinomax_controller()
        logger.info("🎬 [KINOMAX] Контроллер создан за %.1fs", time.time() - step_start)

        step_start = time.time()
        logger.info("🎬 [KINOMAX] Запуск парсинга...")
        controller.run(city=city)
        logger.info("🎬 [KINOMAX] Парсинг завершён за %.1fs", time.time() - step_start)

        elapsed = time.time() - task_start
        logger.info("🎬 [KINOMAX] ✅ Задача завершена за %.1fs", elapsed)
        result = {"parser": "kinomax", "status": "completed", "city": city, "elapsed_seconds": round(elapsed, 1)}
        _emit_parsing_metrics("kinomax", result, task_start)
        return result
    except Exception as e:
        elapsed = time.time() - task_start
        logger.exception("🎬 [KINOMAX] ❌ Ошибка через %.1fs: %s", elapsed, e)
        result = {"parser": "kinomax", "status": "failed", "error": str(e), "elapsed_seconds": round(elapsed, 1)}
        _emit_parsing_metrics("kinomax", result, task_start)
        return result
    finally:
        if controller:
            try:
                controller.main_parser.close_driver()
            except Exception:
                pass
            try:
                controller.session_parser.close_driver()
            except Exception:
                pass
        parsing_in_progress.labels(parser="kinomax").set(0)


@shared_task(name="parsers.run_malibu")
def run_malibu_parser_task():
    task_start = time.time()
    controller = None
    parsing_in_progress.labels(parser="malibu").set(1)
    try:
        logger.info("🎬 [MALIBU] Задача начата")

        step_start = time.time()
        logger.info("🎬 [MALIBU] Создание контроллера...")
        controller = get_malibu_controller()
        logger.info("🎬 [MALIBU] Контроллер создан за %.1fs", time.time() - step_start)

        step_start = time.time()
        logger.info("🎬 [MALIBU] Запуск парсинга...")
        controller.run()
        logger.info("🎬 [MALIBU] Парсинг завершён за %.1fs", time.time() - step_start)

        elapsed = time.time() - task_start
        logger.info("🎬 [MALIBU] ✅ Задача завершена за %.1fs", elapsed)
        result = {"parser": "malibu", "status": "completed", "elapsed_seconds": round(elapsed, 1)}
        _emit_parsing_metrics("malibu", result, task_start)
        return result
    except Exception as e:
        elapsed = time.time() - task_start
        logger.exception("🎬 [MALIBU] ❌ Ошибка через %.1fs: %s", elapsed, e)
        result = {"parser": "malibu", "status": "failed", "error": str(e), "elapsed_seconds": round(elapsed, 1)}
        _emit_parsing_metrics("malibu", result, task_start)
        return result
    finally:
        if controller:
            try:
                controller.main_parser.close_driver()
            except Exception:
                pass
            try:
                controller.session_parser.close_driver()
            except Exception:
                pass
        parsing_in_progress.labels(parser="malibu").set(0)


def run_all_parsers_async(city: str = "Липецк") -> dict:
    celery_configure()
    logger.info("🚀 Отправка задач парсинга в Celery. Город: %s", city)
    kinomax_job = run_kinomax_parser_task.delay(city=city)
    malibu_job = run_malibu_parser_task.delay()
    logger.info("🚀 Задачи отправлены: kinomax=%s, malibu=%s", kinomax_job.id, malibu_job.id)
    return {
        "kinomax_task_id": kinomax_job.id,
        "malibu_task_id": malibu_job.id,
    }


def setup_local_chrome_driver():
    """Настройка Selenium ChromeDriver"""
    try:
        logger.info("Установка/проверка chromedriver...")
        import chromedriver_autoinstaller
        path = chromedriver_autoinstaller.install()
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        service = Service(path)
        driver = webdriver.Chrome(service=service)
        logger.info("ChromeDriver успешно запущен")
        driver_operations.labels(operation="create").inc()
        return driver
    except Exception as e:
        logger.exception("Ошибка инициализации ChromeDriver")
        driver_operations.labels(operation="error").inc()
        raise


if __name__ == "__main__":
    logger.info("=== Локальный запуск парсеров (без Celery) для теста ===")
    try:
        driver_kinomax = setup_local_chrome_driver()
        driver_malibu = setup_local_chrome_driver()

        kinomax = build_kinomax_controller(driver=driver_kinomax)
        malibu = get_malibu_controller(driver=driver_malibu)

        logger.info("Запуск Kinomax...")
        kinomax.run(city="Липецк")

        logger.info("Запуск Malibu...")
        malibu.run()

    except Exception as e:
        logger.exception("Критическая ошибка при локальном запуске")
    finally:
        if 'driver_kinomax' in locals():
            driver_kinomax.quit()
            driver_operations.labels(operation="close").inc()
        if 'driver_malibu' in locals():
            driver_malibu.quit()
            driver_operations.labels(operation="close").inc()
