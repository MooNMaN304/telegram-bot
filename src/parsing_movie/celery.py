"""Celery configuration and tasks for movie parsers.

This module is imported both by:
1. The bot (via admin_commands.py) — should NOT call setup_logging()
2. The celery worker (via celery command) — SHOULD call setup_logging()
"""
import time
import os
import sys
from celery import Celery, shared_task

from src.application.value import get_malibu_controller, build_kinomax_controller
from src.settings import settings
from src.utils.logger import setup_logging, get_logger, set_service_context

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
    except Exception as e:
        logger.error("❌ Ошибка подключения к Redis: %s", e)

    # Проверка БД
    try:
        db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "http://")
        url = urlparse(db_url)
        host = url.hostname
        port = url.port or 5432
        logger.info("Проверка подключения к БД: %s:%s", host, port)
        with socket.create_connection((host, port), timeout=5):
            logger.info("✅ Подключение к БД успешно")
    except Exception as e:
        logger.error("❌ Ошибка подключения к БД: %s", e)

    # Проверка Browserless
    try:
        from urllib.parse import urlparse as _urlparse
        sel_url = _urlparse(settings.REMOTE_SELENIUM_URL)
        host = sel_url.hostname
        port = sel_url.port or 3000
        logger.info("Проверка подключения к Browserless: %s:%s", host, port)
        with socket.create_connection((host, port), timeout=5):
            logger.info("✅ Подключение к Browserless успешно")
    except Exception as e:
        logger.error("❌ Ошибка подключения к Browserless: %s", e)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
    worker_hijack_root_logger=False,
)

def celery_configure():
    logger.info("Celery worker configured on %s", _server_location)
    check_connections()


def _resolve_gigachat_credentials() -> str:
    key = settings.GIGACHAT_API_KEY
    if key.endswith("=="):
        return key
    return key

@shared_task(name="parsers.run_kinomax")
def run_kinomax_parser_task(city: str = "Липецк"):
    task_start = time.time()
    controller = None
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
        return {"parser": "kinomax", "status": "completed", "city": city, "elapsed_seconds": round(elapsed, 1)}
    except Exception as e:
        elapsed = time.time() - task_start
        logger.exception("🎬 [KINOMAX] ❌ Ошибка через %.1fs: %s", elapsed, e)
        return {"parser": "kinomax", "status": "failed", "error": str(e), "elapsed_seconds": round(elapsed, 1)}
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


@shared_task(name="parsers.run_malibu")
def run_malibu_parser_task():
    task_start = time.time()
    controller = None
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
        return {"parser": "malibu", "status": "completed", "elapsed_seconds": round(elapsed, 1)}
    except Exception as e:
        elapsed = time.time() - task_start
        logger.exception("🎬 [MALIBU] ❌ Ошибка через %.1fs: %s", elapsed, e)
        return {"parser": "malibu", "status": "failed", "error": str(e), "elapsed_seconds": round(elapsed, 1)}
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
        return driver
    except Exception as e:
        logger.exception("Ошибка инициализации ChromeDriver")
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
        if 'driver_malibu' in locals():
            driver_malibu.quit()
