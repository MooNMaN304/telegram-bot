import logging
from selenium.webdriver.common.by import By

from src.base.base_parser import BaseParser
from src.parsing_movie.kinomax_cinema.html_utils import extract_films_from_main
from src.parsing_movie.kinomax_cinema.kinomax_settings import kinomax_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


class KinomaxMainPageParser(BaseParser):
    def __init__(
        self,
        driver=None,
        wait_time: int | None = None,
    ):
        super().__init__(driver=driver, wait_time=wait_time)

    def parse_all_movies(self) -> list[dict]:
        """
        Парсит все карточки фильмов на главной странице.
        
        Использует HTML-парсинг через lxml вместо Selenium селекторов,
        чтобы избежать привязки к hash-классам, которые меняются при деплое.
        """
        if not self.driver:
            logger.error("WebDriver не инициализирован")
            return []

        try:
            # Ждём загрузки страницы
            if not self.wait_for_element(
                By.TAG_NAME,
                "section",
                timeout=self.wait_time,
            ):
                logger.warning("Секции не найдены на странице")
                return []

            # Получаем page_source и передаём в функцию парсинга
            page_html = self.driver.page_source
            return extract_films_from_main(page_html)

        except Exception as e:
            logger.exception("Ошибка парсинга главной страницы Kinomax: %s", e)
            return []
