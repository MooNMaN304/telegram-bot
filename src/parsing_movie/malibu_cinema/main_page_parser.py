from selenium.webdriver.common.by import By
from src.base.base_parser import BaseParser
from src.parsing_movie.malibu_cinema.extractor import MalibuMainPageExtractor


class MalibuMainPageParser(BaseParser):
    """Парсинг списка фильмов Malibu с главной страницы"""

    def __init__(self, url: str, css_selector: str, wait_time: int, extractor: MalibuMainPageExtractor, driver=None):
        super().__init__()
        self.url = url
        self.css_selector = css_selector
        self.wait_time = wait_time
        self.extractor = extractor
        

    def parse_all_movies(self) -> list[dict]:
        """Возвращает список фильмов с главной страницы"""
        try:
            self.driver.get(self.url)
            # Ждем загрузки списка фильмов
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.css_selector))
            )

            elements = self.driver.find_elements(By.CSS_SELECTOR, self.css_selector)
            return [self.extractor.parse_movie_card(el) for el in elements]

        except Exception as e:
            print(f"Ошибка при парсинге главной страницы: {e}")
            return []