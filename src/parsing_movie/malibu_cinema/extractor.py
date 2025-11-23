from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from urllib.parse import urlparse


class MalibuMainPageExtractor:
    """Извлечение данных о фильмах Malibu"""

    def __init__(self, selectors: dict):
        self.selectors = selectors

    def parse_movie_card(self, element) -> dict[str, str]:
        """Парсинг карточки фильма на главной странице"""
        text = element.text.split('\n')
        title = text[0] if text else "Неизвестно"
        url = element.get_attribute('href')
        movie_id = self.extract_release_id(url)
        return {"title": title, "url": url, "id_malibu": movie_id}

    @staticmethod
    def extract_release_id(url: str) -> int:
        """Извлекает ID фильма из URL"""
        path = urlparse(url).path
        release_id = path.split('/')[-1]
        try:
            return int(release_id)
        except ValueError:
            return 0
    
    
class MalibuDetailsExtractor:
    """Извлечение деталей фильма Malibu"""

    def __init__(self, selectors: dict):
        self.selectors = selectors

    def parse_movie_details(self, driver) -> dict:
        """Парсинг страницы фильма (детали)"""
        return {
            "description": self._extract_description(driver),
            "poster": self._extract_poster(driver),
            "genre": self._extract_genre(driver),
            "title": self._extract_title(driver)
        }

    def _extract_description(self, driver) -> str | None:
        """Извлечение описания — проверяет несколько селекторов поочередно"""
        selectors = self.selectors.get("description", [])
        description = ""
        
        for selector in selectors:
            try:
                desc_el = driver.find_element(By.CSS_SELECTOR, selector)
                text = desc_el.text.strip()
                if text:
                    description = text
            except NoSuchElementException:
                continue

        return description if description else None

    def _extract_poster(self, driver) -> str | None:
        """Извлечение постера"""
        try:
            poster_el = driver.find_element(By.CSS_SELECTOR, self.selectors["poster"])
            return poster_el.get_attribute("src")
        except (NoSuchElementException, WebDriverException):
            return None

    def _extract_genre(self, driver) -> str | None:
        """Извлечение жанра"""
        try:
            genre_el = driver.find_element(By.CSS_SELECTOR, self.selectors["genre"])
            return genre_el.text.strip()
        except (NoSuchElementException, WebDriverException):
            return None

    def _extract_title(self, driver) -> str | None:
        """Извлечение названия"""
        try:
            title_el = driver.find_element(By.CSS_SELECTOR, self.selectors["title"])
            return title_el.text.strip()
        except (NoSuchElementException, WebDriverException):
            return None
