import logging
from selenium.webdriver.common.by import By
from src.base.base_parser import BaseParser
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings
from src.parsing_movie.malibu_cinema.html_utils import extract_release_cards

logger = logging.getLogger(__name__)


class MalibuMainPageParser(BaseParser):

    def __init__(self, driver=None, wait_time: int | None = None):
        super().__init__(driver=driver, wait_time=wait_time)
        self.settings = malibu_settings

    def parse_all_movies(self) -> list[dict]:
        if not self.driver:
            logger.error("Драйвер не инициализирован")
            return []

        try:
            self.navigate(self.settings.MALIBU_URL)
            self.sleep(1)
            self.press_escape()

            # ждём контейнер (у тебя уже XPath)
            container_xpath = self.settings.MAIN_PAGE_SELECTORS["movies_container_xpath"]

            if not self.wait_for_element(By.XPATH, container_xpath):
                logger.warning("Контейнер фильмов не найден")
                return []

            page_html = self.driver.page_source

            # 🧠 debug кодировка (ТОЛЬКО ДЛЯ ДИАГНОСТИКИ)
            logger.debug("HTML length: %d", len(page_html))
            logger.debug("HTML preview: %s", page_html[:300])

            #release_ids = extract_release_links(page_html)
            movies = extract_release_cards(page_html)


            if not movies:
                logger.warning("Нет релизов на странице")
                return []

            logger.info("Найдено релизов: %d", len(movies))

            # ✔️ ВАЖНО: добавляем url сразу (это потом спасёт тебя)
            # base_url уже добавлен в extract_release_cards

            return movies

            # return [
            #     {
            #         "release_id": rid,
            #         "url": f"{base_url}{rid}",
            #     }
            #     for rid in release_ids
            # ]


        except Exception as e:
            logger.exception("Ошибка при парсинге Malibu main page")
            return []