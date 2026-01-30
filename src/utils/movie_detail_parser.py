import logging
from src.movies.movie_schema import BaseMovieSchema
from src.utils.kino_api.client import KinoAPIClient

logger = logging.getLogger(__name__)


class MovieDetailParser:
    """Получение деталей фильма через внешнее API по названию"""

    def __init__(self, api_client: KinoAPIClient):
        self.api_client = api_client

    def parse_by_title(self, title: str) -> BaseMovieSchema | None:
        try:
            film_data = self.api_client.find_movie_by_title(title)
            if not film_data:
                logger.warning(f"Фильм '{title}' не найден в API")
                return None

            return BaseMovieSchema(
                title=film_data.name_ru or "",
                poster_url=film_data.poster_url or "",
                description=film_data.description or "",
                genres=[g.genre for g in getattr(film_data, "genres", []) if g.genre],
                kinopoisk_id=film_data.film_id,
            )

        except Exception as e:
            logger.error(f"Ошибка получения деталей фильма '{title}': {e}")
            return None
