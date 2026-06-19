from src.db.movies.movie_schema import BaseMovieSchema
from src.utils.kino_api.client import KinoAPIClient
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MovieDetailParser:
    """Получение деталей фильма через внешнее API по названию"""

    def __init__(self, api_client: KinoAPIClient):
        self.api_client = api_client

    def parse_by_title(self, title: str) -> BaseMovieSchema | None:
        logger.info(f"Поиск фильма через API: {title}")

        try:
            film_data = self.api_client.find_movie_by_title(title)

            logger.debug(f"Ответ API для '{title}': {film_data}")

            if not film_data:
                logger.warning(f"Фильм '{title}' не найден в API")
                return None

            logger.info(f"Фильм найден: {film_data.name_ru}")

            # Собираем все данные с API в additional_data
            api_data = {
                "name_en": getattr(film_data, "name_en", None),
                "duration": getattr(film_data, "film_length", None),
                "year": getattr(film_data, "year", None),
                "rating": getattr(film_data, "rating", None),
                "votes_count": getattr(film_data, "votes_count", None),
            }
            # Фильтруем None значения
            api_data = {k: v for k, v in api_data.items() if v is not None}

            return BaseMovieSchema(
                title=film_data.name_ru or "",
                poster_url=film_data.poster_url or "",
                description=film_data.description or "",
                genres=[g.genre for g in getattr(film_data, "genres", []) if g.genre],
                kinopoisk_id=film_data.film_id,
                additional_data=api_data,
            )

        except Exception as e:
            logger.exception(f"Ошибка получения деталей фильма '{title}'")
            return None
