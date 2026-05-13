from src.out.openapi_client.api_client import ApiClient
from src.out.openapi_client.api.films_api import FilmsApi
from src.out.openapi_client.configuration import Configuration
from src.settings import settings

import logging
import time

logger = logging.getLogger(__name__)


class KinoAPIClient:
    def __init__(self):
        logger.info("Инициализация KinoAPIClient")

        self.config = Configuration(
            api_key={"ApiKeyAuth": settings.KINOPOISK_API_KEY}
        )

        # создаём клиент один раз
        self.api_client = ApiClient(self.config)
        self.api = FilmsApi(self.api_client)

    def find_movie_by_title(self, title: str):
        """
        Ищет фильм по названию и возвращает первый результат
        """

        try:
            logger.info(f"Запрос к Kinopoisk API: {title}")
            
            # Задержка для избежания Rate Limit (429)
            time.sleep(0.3)

            response = self.api.api_v21_films_search_by_keyword_get(
                keyword=title,
                page=1
            )

            logger.debug(f"Ответ Kinopoisk API: {response}")

            films = response.films

            if not films:
                logger.warning(f"Фильм не найден в API: {title}")
                return None

            film = films[0]

            logger.info(f"Найден фильм: {film.name_ru}")

            return film

        except Exception:
            logger.exception(f"Ошибка запроса к Kinopoisk API: {title}")
            return None