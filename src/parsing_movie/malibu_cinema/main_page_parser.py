import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.base.base_parser import BaseParser
from src.parsing_movie.malibu_cinema.extractor import MalibuMainPageExtractor

logger = logging.getLogger(__name__)


class MalibuMainPageParser(BaseParser):
    """Парсинг списка фильмов Malibu с главной страницы"""

    def __init__(self, url: str, css_selector: str, extractor: MalibuMainPageExtractor, wait_time: int | None = None):
        super().__init__(wait_time=wait_time)
        self.url = url
        self.css_selector = css_selector
        self.extractor = extractor

    def parse_all_movies(self) -> list[dict]:
        """
        Возвращает список фильмов с главной страницы.
        Использует методы BaseParser для навигации и ожидания.
        """
        if not self.driver:
            logger.error("Драйвер не инициализирован")
            return []

        try:
            # Переходим на страницу
            self.navigate(self.url)

            # Ждём 1 секунду, чтобы подгрузился JS
            time.sleep(1)

            # Нажимаем Escape на случай модальных окон
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            # Ждём появления элементов с фильмами
            if not self.wait_for_element(By.CSS_SELECTOR, self.css_selector):
                logger.warning("Элементы фильмов не найдены на странице")
                return []

            # Получаем все элементы и парсим через extractor
            elements = self.driver.find_elements(By.CSS_SELECTOR, self.css_selector)
            if not elements:
                logger.warning("На странице нет элементов фильмов")
                return []

            return [self.extractor.parse_movie_card(el) for el in elements]

        except Exception as e:
            logger.error(f"Ошибка при парсинге главной страницы: {e}")
            return []
