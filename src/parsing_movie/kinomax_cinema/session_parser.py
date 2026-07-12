from datetime import datetime, timedelta
from typing import List

from selenium.common.exceptions import WebDriverException

from src.base.base_parser import BaseParser
from src.parsing_movie.kinomax_cinema.kinomax_settings import kinomax_settings
from src.parsing_movie.kinomax_cinema.html_utils import extract_order_links_html
from src.utils.gigachat_request import GigaChatScheduleParser
from src.db.sessions.session_schema import SessionSchema
from src.utils.logger import get_logger
from src.utils.metrics import driver_operations

logger = get_logger(__name__)


class KinomaxSessionParser(BaseParser):
    """
    Парсер расписания Kinomax через:
    1. Получение HTML блока с расписанием сеансов
    2. Отправку HTML-текста в GigaChat (Lite)
    3. Конвертацию ответа в SessionSchema
    """

    def __init__(
        self,
        gigachat_parser: GigaChatScheduleParser,
        driver=None,
        wait_time: int | None = None,
    ):
        super().__init__(driver=driver, wait_time=wait_time)
        self.settings = kinomax_settings
        self.gigachat_parser = gigachat_parser

    # ==========================================================
    # URL GENERATION
    # ==========================================================
    def form_urls(self, movie_id: str, days: int = 5) -> List[tuple[str, str]]:
        today = datetime.now().date()
        result = []
        for i in range(days):
            date_obj = today + timedelta(days=i)
            date_str = date_obj.strftime("%Y-%m-%d")
            url = f"{self.settings.KINOMAX_URL}films/{movie_id}/{date_str}"
            result.append((url, date_str))
        return result

    # ==========================================================
    # PUBLIC METHOD
    # ==========================================================
    def parse_sessions(
        self,
        movie_id: str,
        movie_db_id: int | None = None,
        cinema_id: int | None = None,
        days: int = 5,
    ) -> List[SessionSchema]:
        urls = self.form_urls(movie_id, days)
        all_sessions: List[SessionSchema] = []
        consecutive_empty_days = 0
        max_empty_days = 1  # Если 2 дня подряд без сеансов, прекращаем
        
        for url, schedule_date in urls:
            sessions = self._process_single_day(
                url=url,
                schedule_date=schedule_date,
                movie_db_id=movie_db_id,
                cinema_id=cinema_id,
            )
            all_sessions.extend(sessions)
            
            # Проверка: если нет сеансов в этот день
            if not sessions:
                consecutive_empty_days += 1
                if consecutive_empty_days >= max_empty_days:
                    logger.info(
                        f"⏸️ Прекращаем парсинг - {max_empty_days} дня подряд без сеансов"
                    )
                    break
            else:
                # Сбрасываем счётчик, если нашли сеансы
                consecutive_empty_days = 0
        
        return all_sessions

    # ==========================================================
    # SINGLE DAY PROCESSING
    # ==========================================================
    def _process_single_day(
        self,
        url: str,
        schedule_date: str,
        movie_db_id: int | None,
        cinema_id: int | None,
    ) -> List[SessionSchema]:
        return self._process_single_day_with_retry(
            url, schedule_date, movie_db_id, cinema_id, retry_count=0,
        )

    def _process_single_day_with_retry(
        self,
        url: str,
        schedule_date: str,
        movie_db_id: int | None,
        cinema_id: int | None,
        retry_count: int = 0,
    ) -> List[SessionSchema]:
        max_retries = 1  # пересоздаём драйвер максимум 1 раз за день
        try:
            logger.info(f"Открытие страницы сеансов: {url}")
            self.navigate(url)

            if not self.driver:
                logger.warning("Драйвер не инициализирован")
                return []

            page_html = self.driver.page_source
            html_content = extract_order_links_html(page_html)

            # extract_order_links_html вернёт пустую строку если:
            # 1. Есть сообщение о пустом расписании
            # 2. Нет ссылок с /order/
            if not html_content:
                logger.info(f"⏸️ Нет сеансов {schedule_date}: {url}")
                return []

            logger.debug(f"Получен HTML расписания, длина: {len(html_content)} символов")

            # Передача в gigachat_parser
            ai_result = self.gigachat_parser.parse_cinema_schedule(html_content)

            if not ai_result or not ai_result.sessions:
                logger.info(f"GigaChat не нашёл сеансов для {schedule_date}")
                return []

            return self._convert_ai_sessions(
                ai_result.sessions,
                schedule_date,
                movie_db_id,
                cinema_id,
            )
        except WebDriverException as e:
            error_msg = str(e).lower()
            is_session_lost = (
                "couldn't access session" in error_msg
                or "session not created" in error_msg
                or "timeout" in error_msg
            )
            if is_session_lost and retry_count < max_retries:
                logger.warning(
                    "⚠️ Сессия WebDriver потеряна для %s (%s). "
                    "Пересоздаём драйвер и пробуем снова (попытка %d)...",
                    schedule_date, url, retry_count + 1,
                )
                self.close_driver()
                driver_operations.labels(operation="close").inc()
                import time
                time.sleep(2)
                self._setup_driver()
                driver_operations.labels(operation="restart").inc()
                return self._process_single_day_with_retry(
                    url, schedule_date, movie_db_id, cinema_id,
                    retry_count=retry_count + 1,
                )
            logger.exception(
                "❌ Ошибка WebDriver для %s (%s): %s", schedule_date, url, e,
            )
            return []
        except Exception as e:
            logger.exception(f"Ошибка обработки дня {schedule_date} ({url}): {e}")
            return []

    # ==========================================================
    # CONVERT AI RESPONSE → SessionSchema
    # ==========================================================
    def _convert_ai_sessions(
        self,
        raw_sessions,
        schedule_date: str,
        movie_db_id: int | None,
        cinema_id: int | None,
    ) -> List[SessionSchema]:
        result: List[SessionSchema] = []
        for s in raw_sessions:
            try:
                # Предполагаем, что time в формате "HH:MM"
                dt = datetime.strptime(
                    f"{schedule_date} {s.time}",
                    "%Y-%m-%d %H:%M",
                )
                session = SessionSchema(
                    session_id=None,
                    date=dt,
                    movie_id=movie_db_id,
                    cinema_id=cinema_id,
                    updated_at=datetime.now(),
                )
                result.append(session)
            except Exception as e:
                logger.warning(f"Ошибка сборки сеанса из AI-ответа: {e} | данные: {s}")
        return result




