#!/usr/bin/env python3
"""
Скрипт для локального запуска парсера Malibu без Docker контейнеров
Использует локальный ChromeDriver
"""

import logging
import sys
import os

# Добавляем корневую папку в path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import setup_logging, get_logger
from src.application.value import get_malibu_controller

from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium import webdriver

logger = get_logger(__name__)


def setup_local_chrome_driver():
    """Настройка Selenium ChromeDriver для локального использования"""
    try:
        logger.info("Установка/проверка chromedriver...")
        path = chromedriver_autoinstaller.install()
        service = Service(path)
        driver = webdriver.Chrome(service=service)
        logger.info("✓ ChromeDriver успешно запущен")
        return driver
    except Exception as e:
        logger.exception("✗ Ошибка инициализации ChromeDriver")
        raise


def run_malibu_parser_local():
    """Запуск парсера Malibu локально"""
    driver = None
    try:
        logger.info("=" * 80)
        logger.info("ЗАПУСК MALIBU ПАРСЕРА (ЛОКАЛЬНО БЕЗ DOCKER)")
        logger.info("=" * 80)

        # Инициализируем локальный ChromeDriver
        driver = setup_local_chrome_driver()

        # Создаём контроллер с локальным драйвером
        malibu_controller = get_malibu_controller(driver=driver)

        # Запускаем парсер
        logger.info("Начинаю парсинг Malibu...")
        malibu_controller.run()

        logger.info("=" * 80)
        logger.info("✓ MALIBU ПАРСЕР УСПЕШНО ЗАВЕРШЁН")
        logger.info("=" * 80)
        return True

    except Exception as e:
        logger.exception(f"✗ Ошибка при запуске парсера Malibu: {e}")
        return False

    finally:
        # Закрываем браузер
        if driver:
            try:
                driver.quit()
                logger.info("ChromeDriver закрыт")
            except Exception as e:
                logger.warning(f"Ошибка при закрытии ChromeDriver: {e}")


if __name__ == "__main__":
    setup_logging()
    success = run_malibu_parser_local()
    sys.exit(0 if success else 1)
