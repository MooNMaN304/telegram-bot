# src/base/base_parser.py
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from src.settings import settings

logger = logging.getLogger(__name__)

class BaseParser:
    def __init__(self):
        self.driver = None
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

    def _escape_pressing(self):
        """Нажатие ESC для закрытия рекламы"""
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()

    def _wait_for_page_load(self, seconds: int = 10):
        wait_time = seconds or settings.WAIT_PAGE_LOAD
        time.sleep(seconds)

    def _close_driver(self):
        """Закрывает браузер"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception as e:
            logger.error(f"Ошибка при закрытии драйвера: {e}")
