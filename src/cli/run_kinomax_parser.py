#!/usr/bin/env python3
"""
Локальный запуск парсера Kinomax (с GigaChat)
"""

import logging
import sys
import os

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import setup_logging, get_logger
from src.parsing_movie.celery import _build_kinomax_controller, setup_local_chrome_driver

logger = get_logger(__name__)


def run_kinomax_parser_local(city: str = "Липецк"):
    driver = None

    try:
        logger.info("=" * 80)
        logger.info("ЗАПУСК KINOMAX ПАРСЕРА (GigaChat)")
        logger.info("=" * 80)

        # 🔥 ChromeDriver
        driver = setup_local_chrome_driver()

        # 🔥 контроллер
        controller = _build_kinomax_controller(driver=driver)

        # 🔥 запуск
        logger.info("Начинаю парсинг Kinomax...")
        controller.run(city=city)

        logger.info("=" * 80)
        logger.info("✓ KINOMAX ПАРСЕР УСПЕШНО ЗАВЕРШЁН")
        logger.info("=" * 80)

        return True

    except Exception as e:
        logger.exception(f"✗ Ошибка Kinomax парсера: {e}")
        return False

    finally:
        if driver:
            try:
                driver.quit()
                logger.info("ChromeDriver закрыт")
            except Exception as e:
                logger.warning(f"Ошибка закрытия ChromeDriver: {e}")


if __name__ == "__main__":
    setup_logging()
    success = run_kinomax_parser_local()
    sys.exit(0 if success else 1)