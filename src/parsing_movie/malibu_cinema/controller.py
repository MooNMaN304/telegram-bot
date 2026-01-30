import logging

from src.cinemas.cinema_repository import CinemaRepository
from src.cinemas.init_cinemas import init_cinemas
from src.movies.movie_repository import MovieRepository
from src.sessions.session_repository import SessionRepository

from src.parsing_movie.malibu_cinema.main_page_parser import MalibuMainPageParser
from src.parsing_movie.malibu_cinema.session_parser import MalibuSessionParser
from src.utils.movie_detail_parser import MovieDetailParser

logger = logging.getLogger(__name__)


class MalibuController:
    def __init__(
        self,
        movie_repo: MovieRepository,
        cinema_repo: CinemaRepository,
        session_repo: SessionRepository,
        main_parser: MalibuMainPageParser,
        movie_detail_parser: MovieDetailParser,
        session_parser: MalibuSessionParser,
    ):
        self.movie_repo = movie_repo
        self.cinema_repo = cinema_repo
        self.session_repo = session_repo
        self.main_parser = main_parser
        self.movie_detail_parser = movie_detail_parser
        self.session_parser = session_parser

    def get_malibu_cinema_id(self) -> int:
        cinema = self.cinema_repo.get_by_name("Малибу")
        if cinema:
            return cinema.id

        init_cinemas(self.cinema_repo.db)
        cinema = self.cinema_repo.get_by_name("Малибу")
        if cinema:
            return cinema.id

        raise ValueError("Не удалось получить ID кинотеатра Малибу")

    def malibu_movies_record(self):
        malibu_cinema_id = self.get_malibu_cinema_id()

        logger.info("Запуск парсера фильмов Малибу...")
        films = self.main_parser.parse_all_movies()

        if not films:
            logger.warning("Парсер не вернул фильмов.")
            return

        logger.info(f"Найдено фильмов: {len(films)}")

        for idx, film_data in enumerate(films, start=1):
            title = film_data.get("title")
            malibu_url = film_data.get("url")

            logger.info(f"[{idx}/{len(films)}] Фильм: {title}")

            if not title:
                logger.warning(f"✗ Название фильма отсутствует, пропускаем запись: {film_data}")
                continue

            # 1️⃣ Детали фильма (общие)
            movie_details = self.movie_detail_parser.parse_by_title(title)
            if not movie_details:
                logger.warning(f"✗ Не удалось получить детали '{title}'")
                continue

            # 2️⃣ Malibu-specific данные
            malibu_movie_id = self._extract_malibu_movie_id(malibu_url)

            # 3️⃣ Сохранение
            movie = self.movie_repo.get_or_create(
                name=movie_details.title,
                cinema_id=malibu_cinema_id,
                defaults={
                    "description": movie_details.description,
                    "genre": ", ".join(movie_details.genres),
                    "poster": movie_details.poster_url,
                    "kinopoisk_id": movie_details.kinopoisk_id,
                    "additional_data": {
                        "url": malibu_url,
                        "id_malibu": malibu_movie_id,
                    },
                    "related_movies": {
                        malibu_cinema_id: malibu_movie_id
                    } if malibu_movie_id else {},
                },
            )

            logger.info(f"✓ Фильм сохранён: id={movie.id}")

            # 4️⃣ Сеансы
            self.update_movie_sessions(movie, malibu_cinema_id)

    def update_movie_sessions(self, movie, cinema_id: int):
        movie_url = movie.additional_data.get("url")
        if not movie_url:
            return

        urls = self.session_parser.form_urls(movie_url)

        for url in urls:
            sessions = self.session_parser.parse_sessions(
                driver=self.main_parser.driver,
                url=url,
                movie_id=movie.id,
                cinema_id=cinema_id
            )

            for session in sessions:
                self.session_repo.get_or_create(
                    session_id=session.session_id,
                    cinema_id=session.cinema_id,
                    defaults={
                        "date": session.date,
                        "movie_id": session.movie_id,
                    },
                )

        logger.info(f"Сеансы обновлены для '{movie.name}'")

    # ----------------------
    # Приватный метод
    # ----------------------
    def _extract_malibu_movie_id(self, url: str) -> str | None:
        """Извлечение ID фильма из URL Малибу"""
        if not url:
            return None
        parts = url.rstrip("/").split("/")
        return parts[-1] if parts else None
