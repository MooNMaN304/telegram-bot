import logging
from sqlalchemy.orm import Session

from src.cinemas.cinema_repository import CinemaRepository
from src.cinemas.init_cinemas import init_cinemas
from src.movies.movie_repository import MovieRepository
from src.movies.movie_model import MovieModel
from src.sessions.session_repository import SessionRepository

from src.parsing_movie.malibu_cinema.main_page_parser import MalibuMainPageParser
from src.parsing_movie.malibu_cinema.details_parser import MalibuDetailsParser
from src.parsing_movie.malibu_cinema.session_parser import MalibuSessionParser

logger = logging.getLogger(__name__)


class MalibuService:
    def __init__(
        self,
        db: Session,
        movie_repo: MovieRepository,
        cinema_repo: CinemaRepository,
        session_repo: SessionRepository,
        main_parser: MalibuMainPageParser,
        details_parser: MalibuDetailsParser,
        session_parser: MalibuSessionParser,
    ):
        self.db = db
        self.movie_repo = movie_repo
        self.cinema_repo = cinema_repo
        self.session_repo = session_repo
        self.main_parser = main_parser
        self.details_parser = details_parser
        self.session_parser = session_parser

    def get_malibu_cinema_id(self) -> int:
        """Получаем ID кинотеатра 'Малибу' из базы"""
        cinema = self.cinema_repo.get_by_name("Малибу")
        if cinema:
            return cinema.id

        init_cinemas(self.db)
        cinema = self.cinema_repo.get_by_name("Малибу")
        if cinema:
            return cinema.id

        raise ValueError("Не удалось получить ID кинотеатра Малибу")

    def malibu_movies_record(self, malibu_cinema_id: int):
        """Парсинг фильмов с сайта Малибу и запись их в БД"""
        logger.info("Запуск парсера фильмов Малибу...")

        films = self.main_parser.parse_all_movies()
        if not films:
            logger.warning("Парсер не вернул фильмов.")
            return

        logger.info(f"Найдено фильмов для обработки: {len(films)}")

        for idx, film_data in enumerate(films, start=1):
            logger.info(f"\n{'='*60}")
            logger.info(f"[{idx}/{len(films)}] Обработка фильма по ссылке: {film_data['url']}")
            logger.info(f"{'='*60}")
            
            # Сначала парсим детали с полной информацией (включая название)
            logger.info(f"[{idx}/{len(films)}] Шаг 1: Парсинг деталей фильма...")
            movie_schema = self.details_parser.parse_details(film_data["url"])
            
            if not movie_schema or not movie_schema.title:
                logger.warning(f"[{idx}/{len(films)}] ✗ Не удалось получить название фильма из {film_data['url']}")
                continue
            
            logger.info(f"[{idx}/{len(films)}] ✓ Получено название: {movie_schema.title}")
            
            # ТЕПЕРЬ сохраняем фильм в БД с полными данными
            movie = self.movie_repo.get_or_create(
                name=movie_schema.title,
                cinema_id=malibu_cinema_id,
                defaults={
                    "additional_data": {
                        "url": film_data["url"],
                        "id_malibu": film_data["id_malibu"],
                    },
                    "description": movie_schema.description,
                    "genre": ", ".join(movie_schema.genres),
                    "poster": movie_schema.poster_url,
                },
            )

            logger.info(f"[{idx}/{len(films)}] ✓ Фильм сохранён в БД: id={movie.id}")
            
            # Теперь парсим расписание
            logger.info(f"[{idx}/{len(films)}] Шаг 2: Парсинг расписания...")
            self.update_movie_sessions(movie, malibu_cinema_id)
            
            logger.info(f"[{idx}/{len(films)}] ✓ Фильм полностью обработан\n")

    def update_movie_sessions(self, movie: MovieModel, cinema_id: int):
        """Парсинг и сохранение расписания фильма на 5 дней"""
        logger.info(f"Парсинг расписания фильма '{movie.name}'...")

        movie_url = movie.additional_data.get("url")
        if not movie_url:
            return

        urls = self.session_parser.form_urls(movie_url)

        for url in urls:
            logger.info(f"Парсим расписание по ссылке: {url}")
            sessions = self.session_parser.parse_sessions(
                driver=self.main_parser.driver,
                url=url,
                movie_id=movie.id,
                cinema_id=cinema_id
            )

            for session_schema in sessions:
                self.session_repo.get_or_create(
                    session_id=session_schema.session_id,
                    cinema_id=session_schema.cinema_id,
                    defaults={
                        "date": session_schema.date,
                        "movie_id": session_schema.movie_id,
                    },
                )

        logger.info(f"Сеансы фильма '{movie.name}' обновлены")

# найти на гите template шаблон для использования