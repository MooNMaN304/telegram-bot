import logging
import os
from celery import Celery, shared_task

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

from src.application.value import get_malibu_controller, build_kinomax_controller
from src.settings import settings
from src.utils.logger import setup_logging, get_logger, set_service_context

# Настройка логирования для Celery worker
service_name = os.getenv("SERVICE_NAME", "celery-worker")
server_location = os.getenv("SERVER_LOCATION", "unknown")
setup_logging(service_name=service_name, server_location=server_location)
set_service_context(service_name, server_location)

logger = get_logger(__name__)


celery_app = Celery(
    "parsers",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

def celery_configure():
    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="Europe/Moscow",
        enable_utc=True,
    )
    logger.info(f"Celery worker configured on {server_location}")


def _resolve_gigachat_credentials() -> str:
    key = settings.GIGACHAT_API_KEY
    if key.endswith("=="):
        return key
    return key

@shared_task(name="parsers.run_kinomax")
def run_kinomax_parser_task(city: str = "Липецк"):
    try:
        controller = build_kinomax_controller()
        logger.info(f"Запуск парсинга Kinomax для города: {city}")
        controller.run(city=city)
        return {"parser": "kinomax", "status": "completed", "city": city}
    except Exception as e:
        logger.exception("Ошибка в run_kinomax_parser_task")
        return {"parser": "kinomax", "status": "failed", "error": str(e)}
    finally:
        # Закрываем драйверы парсеров, чтобы избежать утечки ресурсов
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
    try:
        controller = get_malibu_controller()
        logger.info("Запуск парсинга Malibu")
        controller.run()
        return {"parser": "malibu", "status": "completed"}
    except Exception as e:
        logger.exception("Ошибка в run_malibu_parser_task")
        return {"parser": "malibu", "status": "failed", "error": str(e)}
    finally:
        # Закрываем драйверы парсеров, чтобы избежать утечки ресурсов
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
    kinomax_job = run_kinomax_parser_task.delay(city=city)
    malibu_job = run_malibu_parser_task.delay()
    return {
        "kinomax_task_id": kinomax_job.id,
        "malibu_task_id": malibu_job.id,
    }


def setup_local_chrome_driver():
    """Настройка Selenium ChromeDriver"""
    try:
        logger.info("Установка/проверка chromedriver...")
        path = chromedriver_autoinstaller.install()
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
        driver_malibu = setup_local_chrome_driver()  # отдельный драйвер для параллельности

        kinomax = build_kinomax_controller(driver=driver_kinomax)
        malibu = get_malibu_controller(driver=driver_malibu)

        logger.info("Запуск Kinomax...")
        kinomax.run(city="Липецк")

        logger.info("Запуск Malibu...")
        malibu.run()

    except Exception as e:
        logger.exception("Критическая ошибка при локальном запуске")
    finally:
        # Закрываем драйверы, чтобы не висели процессы
        if 'driver_kinomax' in locals():
            driver_kinomax.quit()
        if 'driver_malibu' in locals():
            driver_malibu.quit()
            
			
