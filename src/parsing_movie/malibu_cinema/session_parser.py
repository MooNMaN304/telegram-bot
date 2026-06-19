from datetime import datetime, timedelta

from selenium.webdriver.common.by import By

from src.base.base_parser import BaseParser
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings
from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor
from src.db.sessions.session_schema import SessionSchema
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MalibuSessionParser(BaseParser):
    """Парсер расписания (сеансов) фильма в кинотеатре Malibu"""

    def __init__(
        self,
        driver=None,
        wait_time: int | None = None,
    ):
        super().__init__(driver=driver, wait_time=wait_time)
        self.extractor = MalibuSessionExtractor(malibu_settings.SESSION_SELECTORS["malibu"])
        self.selectors = malibu_settings.SESSION_SELECTORS["malibu"]
        self.parsing_options = malibu_settings.SESSION_PARSING_OPTIONS

    def form_urls(self, movie_url: str, days: int = 5) -> list[str]:
        """Генерирует ссылки на расписание (сегодня + N дней)"""
        base_url = movie_url.split("?")[0]
        today = datetime.now().date()

        return [
            f"{base_url}?date={(today + timedelta(days=i)).strftime('%Y-%m-%d')}"
            for i in range(days)
        ]

    def parse_sessions(
        self,
        url: str,
        movie_id: int | None = None,
        cinema_id: int | None = None,
    ) -> list[SessionSchema]:
        """Парсит все сеансы на странице расписания с ранним выходом если нет сеансов."""
        sessions: list[SessionSchema] = []

        try:
            self.navigate(url)
            self.sleep(2)  # Ожидание загрузки JS

            # 🔥 ранний выход - проверка наличия data-seance-id ПЕРЕД extractor
            seance_elements = self.driver.find_elements(By.XPATH, ".//div[@data-seance-id]")
            if not seance_elements:
                logger.info("Нет seance-id элементов: %s", url)
                return []

            if not self.wait_for_element(
                By.CSS_SELECTOR,
                self.selectors["schedule_block"],
            ):
                logger.warning("Блоки сеансов не найдены: %s", url)
                return []

            schedule_blocks = self.driver.find_elements(
                By.CSS_SELECTOR,
                self.selectors["schedule_block"],
            )

            for block in schedule_blocks:
                raw_sessions = self.extractor.parse_schedule_block(block)

                for raw in raw_sessions:
                    session_datetime = self._build_datetime(url, raw.get("time"))
                    session = self._build_session_schema(
                        raw,
                        session_datetime,
                        movie_id,
                        cinema_id,
                    )
                    if session:
                        sessions.append(session)

        except Exception as e:
            logger.warning("Ошибка при парсинге расписания %s: %s", url, e)

        return sessions

    def parse_sessions_with_stop(
        self,
        movie_url: str,
        movie_id: int | None,
        cinema_id: int | None,
        days: int | None = None,
    ) -> list[SessionSchema]:
        """
        Парсит сеансы с остановкой если нет сеансов несколько дней подряд.
        
        Архитектурная правка: вместо простого цикла по дням,
        добавляем логику "early stop" для оптимизации.
        
        Args:
            movie_url: Базовая ссылка на фильм
            movie_id: ID фильма
            cinema_id: ID кинотеатра
            days: Количество дней для проверки (если None - используем из settings)
            
        Returns:
            Все найденные сеансы до остановки
        """
        if days is None:
            days = self.parsing_options.get("days_to_check", 5)

        urls = self.form_urls(movie_url, days)
        all_sessions: list[SessionSchema] = []
        empty_days = 0
        max_empty_days = self.parsing_options.get("max_empty_days", 2)

        for url in urls:
            try:
                sessions = self.parse_sessions(
                    url=url,
                    movie_id=movie_id,
                    cinema_id=cinema_id,
                )

                if not sessions:
                    empty_days += 1
                    logger.info("⛔ Нет сеансов на дату: %s", url)

                    if empty_days >= max_empty_days:
                        logger.info(
                            "⏹️ Прекращаем парсинг — %d дня подряд без сеансов",
                            max_empty_days,
                        )
                        break
                else:
                    empty_days = 0
                    logger.info("📅 %s → найдено сеансов: %d", url, len(sessions))
                    all_sessions.extend(sessions)

            except Exception as e:
                logger.warning("Ошибка при парсинге %s: %s", url, e)
                empty_days += 1
                if empty_days >= max_empty_days:
                    logger.info(
                        "⏹️ Прекращаем парсинг — %d ошибок подряд",
                        max_empty_days,
                    )
                    break

        return all_sessions

    def _build_session_schema(
        self,
        data: dict,
        session_datetime: datetime,
        movie_id: int | None,
        cinema_id: int | None,
    ) -> SessionSchema | None:
        """Создание и валидация SessionSchema"""
        try:
            return SessionSchema(
                session_id=data["session_id"],
                date=session_datetime,
                movie_id=movie_id,
                cinema_id=cinema_id,
                updated_at=datetime.now(),
            )
        except ValueError as e:
            logger.warning("Ошибка валидации сеанса: %s, данные=%s", e, data)
            return None

    @staticmethod
    def _build_datetime(url: str, time_str: str) -> datetime:
        """Комбинирует дату из URL и время сеанса"""
        try:
            if not time_str or ":" not in time_str:
                return datetime.now()

            date_part = url.split("date=")[1]
            base_date = datetime.strptime(date_part, "%Y-%m-%d").date()
            hours, minutes = map(int, time_str.split(":"))
            return datetime.combine(base_date, datetime.min.time()).replace(
                hour=hours,
                minute=minutes,
            )
        except (ValueError, IndexError):
            return datetime.now()
