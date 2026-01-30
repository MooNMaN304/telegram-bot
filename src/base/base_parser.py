# src/base/base_parser.py
import time
import logging
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from src.settings import settings

logger = logging.getLogger(__name__)


class BaseParser:
    """Базовый класс для всех парсеров с Selenium"""

    def __init__(self, wait_time: int | None = None):
        self.driver: webdriver.Chrome | None = None
        self.wait_time = wait_time or getattr(settings, "WAIT_PAGE_LOAD", 10)
        self._setup_driver()

    def _setup_driver(self):
        """Настройка Selenium ChromeDriver"""
        try:
            path = chromedriver_autoinstaller.install()
            service = Service(path)
            self.driver = webdriver.Chrome(service=service)
            logger.info("ChromeDriver успешно запущен")
        except Exception as e:
            logger.error(f"Ошибка при настройке драйвера: {e}")
            raise

    def press_escape(self):
        """Нажатие ESC для закрытия рекламы/модальных окон"""
        if not self.driver:
            return
        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            logger.debug("ESC нажат")
        except Exception as e:
            logger.warning(f"Не удалось нажать ESC: {e}")

    def wait_for_element(self, by, locator, timeout: int | None = None):
        """Явное ожидание появления элемента на странице"""
        if not self.driver:
            return False
        wait_time = timeout or self.wait_time
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, locator))
            )
            return True
        except TimeoutException:
            logger.warning(f"Элемент не найден: {locator}")
            return False

    def sleep(self, seconds: int):
        """Пауза для страницы, fallback к time.sleep"""
        logger.debug(f"Сон {seconds} секунд")
        time.sleep(seconds)

    def navigate(self, url: str):
        """Переход по URL с паузой ожидания"""
        if not self.driver:
            return
        logger.info(f"Переход на страницу: {url}")
        self.driver.get(url)
        self.sleep(1)  # Можно увеличить или использовать wait_for_element в наследниках

    def close_driver(self):
        """Закрывает браузер"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("ChromeDriver закрыт")
            except Exception as e:
                logger.error(f"Ошибка при закрытии драйвера: {e}")
            finally:
                self.driver = None

    @contextmanager
    def driver_context(self):
        """Контекстный менеджер для автоматического закрытия драйвера"""
        try:
            yield self.driver
        finally:
            self.close_driver()
