# src/base/base_parser.py
import time
import logging
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
)

#import chromedriver_autoinstaller
from src.settings import settings

logger = logging.getLogger(__name__)


class BaseParser:
    """Базовый класс для всех Selenium-парсеров"""

    def __init__(self, driver=None, wait_time: int | None = None):
        self.driver = driver
        self.wait_time = wait_time or getattr(settings, "WAIT_PAGE_LOAD", 10)

        if self.driver is None:
            self._setup_driver()
        else:
            logger.debug("Используется переданный драйвер")

    def _setup_driver(self):
        try:
            remote_url = settings.REMOTE_SELENIUM_URL

            if not remote_url:
                raise ValueError("REMOTE_SELENIUM_URL не задан")

            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            self.driver = webdriver.Remote(
                command_executor=remote_url,
                options=options,
            )

            logger.info("Remote Chrome подключен")

        except Exception as e:
            logger.error(f"Ошибка Remote драйвера: {e}")
            raise

    # ---------- базовые действия ----------

    def navigate(self, url: str):
        """Переход по URL с небольшой паузой"""
        if not self.driver:
            return
        logger.info(f"Переход на страницу: {url}")
        self.driver.get(url)
        self.sleep(1)

    def sleep(self, seconds: int):
        """Пауза (fallback к time.sleep)"""
        logger.debug(f"Сон {seconds} секунд")
        time.sleep(seconds)

    def press_escape(self):
        """Нажатие ESC (закрытие рекламы/модалок)"""
        if not self.driver:
            return
        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            logger.debug("ESC нажат")
        except WebDriverException as e:
            logger.warning(f"Не удалось нажать ESC: {e}")

    # ---------- ожидания и клики ----------

    def wait_for_element(self, by, locator, timeout: int | None = None) -> bool:
        """Ожидание появления элемента"""
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

    def click(self, by, locator, timeout: int | None = None) -> bool:
        """
        Универсальный безопасный клик:
        - ждёт кликабельность
        - логирует
        - не падает
        """
        if not self.driver:
            return False

        wait_time = timeout or self.wait_time

        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable((by, locator))
            )
            element.click()
            logger.debug(f"Клик по элементу: {locator}")
            return True

        except TimeoutException:
            logger.warning(f"Не удалось кликнуть (timeout): {locator}")
            return False

        except StaleElementReferenceException:
            logger.warning(f"Элемент устарел: {locator}")
            return False

        except WebDriverException as e:
            logger.warning(f"Ошибка клика по {locator}: {e}")
            return False

    def click_by_text(self, text: str, tag: str = "*", timeout: int | None = None) -> bool:
        """Клик по элементу с заданным текстом"""
        xpath = f"//{tag}[contains(normalize-space(), '{text}')]"
        return self.click(By.XPATH, xpath, timeout)

    def element_exists(self, by, locator) -> bool:
        """Проверка наличия элемента без ожидания"""
        if not self.driver:
            return False
        try:
            self.driver.find_element(by, locator)
            return True
        except WebDriverException:
            return False

    # ---------- жизненный цикл ----------

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
