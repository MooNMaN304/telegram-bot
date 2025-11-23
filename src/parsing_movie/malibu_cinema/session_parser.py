import logging

from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from src.base.base_parser import BaseParser
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings
from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor
from src.parsing_movie.malibu_cinema.schemas import MalibuSessionSchema

logger = logging.getLogger(__name__)


class MalibuSessionParser(BaseParser):
    """Парсер расписания (сеансов) фильма в кинотеатре Malibu"""

    def __init__(self, extractor: MalibuSessionExtractor):
        # НЕ вызываем super().__init__() - используем драйвер из параметра parse_sessions()
        self.driver = None  # Инициализируем как None, будет передан в parse_sessions()
        self.selectors = malibu_settings.SESSION_SELECTORS["malibu"]
        self.extractor = extractor

    def form_urls(self, movie_url: str) -> list[str]:
        """Генерирует 5 ссылок (сегодня + 4 дня)"""
        base_url = movie_url.split("?")[0]
        today = datetime.now().date()
        return [
            f"{base_url}?date={(today + timedelta(days=i)).strftime('%Y-%m-%d')}"
            for i in range(5)
        ]

    def parse_sessions(self, driver, url: str, movie_id: int = None, cinema_id: int = None) -> list[MalibuSessionSchema]:
        """Парсит все сеансы и возвращает список валидированных схем"""
        sessions = []

        try:
            # Переходим по ссылке расписания конкретного дня
            driver.get(url)

            # Ждём подгрузку блока с сеансами
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.selectors["schedule_block"]))
            )

            schedule_blocks = driver.find_elements(By.CSS_SELECTOR, self.selectors["schedule_block"])

            for block in schedule_blocks:
                block_sessions = self.extractor.parse_schedule_block(block)
                
                for session_data in block_sessions:
                    session_datetime = self._extract_datetime_from_url(url, session_data["time"])
                    validated_session = self._validate_session_data(
                        session_data, session_datetime, movie_id, cinema_id
                    )
                    if validated_session:
                        sessions.append(validated_session)

        except Exception as e:
            logger.warning(f"Ошибка при парсинге расписания {url}: {e}")

        return sessions

    def _validate_session_data(self, session_data: dict, session_datetime: datetime, 
                             movie_id: int = None, cinema_id: int = None) -> MalibuSessionSchema | None:
        """Валидация данных сеанса через Pydantic схему"""
        try:
            return MalibuSessionSchema(
                session_id=session_data["session_id"],
                date=session_datetime,
                movie_id=movie_id,
                cinema_id=cinema_id,
                updated_at=datetime.now()
            )
        except Exception as e:
            logger.warning(f"Ошибка валидации данных сеанса: {e}, данные: {session_data}")
            return None

    @staticmethod
    def _extract_datetime_from_url(url: str, seance_time: str) -> datetime:
        """Извлекает дату из URL и комбинирует её со временем сеанса."""
        try:
            date_str = url.split("date=")[1]
            base_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            hours, minutes = map(int, seance_time.split(":"))
            return datetime.combine(base_date, datetime.min.time()).replace(hour=hours, minute=minutes)
        except Exception:
            return datetime.now()