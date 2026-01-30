# import logging
# from typing import Optional
# from src.parsing_movie.malibu_cinema.schemas import MalibuMovieSchema
# from src.parsing_movie.kino_api.client import KinoAPIClient

# logger = logging.getLogger(__name__)

# class MalibuDetailsParser:
#     """Получение деталей фильма Malibu через API по названию"""

#     def __init__(self, api_client: KinoAPIClient, malibu_cinema_id: int):
#         self.api_client = api_client
#         self.malibu_cinema_id = malibu_cinema_id  # ID кинотеатра Малибу для related_movies

#     def parse_details_by_title(self, title: str, malibu_url: Optional[str] = None) -> MalibuMovieSchema | None:
#         """
#         Получение деталей фильма по названию через API.
#         malibu_url — URL фильма на сайте Малибу, нужен для извлечения id_malibu
#         """
#         try:
#             film_data = self.api_client.find_movie_by_title(title)
#             if not film_data:
#                 logger.warning(f"Фильм '{title}' не найден в API")
#                 return None

#             # id фильма на сайте Малибу
#             id_malibu = self._extract_movie_id_from_url(malibu_url) if malibu_url else None

#             return MalibuMovieSchema(
#                 title=film_data.nameRu or "",
#                 url=malibu_url or "",
#                 poster_url=film_data.posterUrl or "",
#                 description=film_data.description or "",
#                 genres=[g.genre for g in getattr(film_data, "genres", []) if g.genre],
#                 kinopoisk_id=getattr(film_data, "filmId", None),
#                 id_malibu=id_malibu,
#                 related_movies={self.malibu_cinema_id: id_malibu} if id_malibu else {}
#             )

#         except Exception as e:
#             logger.error(f"Ошибка при получении деталей фильма '{title}': {e}")
#             return None

#     @staticmethod
#     def _extract_movie_id_from_url(url: str) -> str:
#         """Извлекает ID фильма из URL"""
#         try:
#             parts = url.rstrip("/").split('/')
#             return parts[-1] if parts else ""
#         except Exception:
#             return ""
