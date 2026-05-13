# src/parsing_movie/kinomax_cinema/controller.py

import logging
from typing import Optional

from selenium.webdriver.common.by import By

from src.db.cinemas.cinema_repository import CinemaRepository
from src.db.movies.movie_repository import MovieRepository
from src.db.sessions.session_repository import SessionRepository
from src.parsing_movie.abstract.controller import AbstractController
from src.parsing_movie.kinomax_cinema.utils import extract_kinomax_id

from src.parsing_movie.kinomax_cinema.main_page_parser import (
    KinomaxMainPageParser,
)
from src.parsing_movie.kinomax_cinema.session_parser import (
    KinomaxSessionParser,
)
from src.parsing_movie.kinomax_cinema.kinomax_settings import (
    kinomax_settings,
)

from src.utils.movie_detail_parser import MovieDetailParser
from src.db.cinema_movie.cinema_movie_repository import CinemaMovieRepository


logger = logging.getLogger(__name__)


class KinomaxController(AbstractController):
    """
    Оркестратор Kinomax.

    Ответственность:
    - выбрать город
    - собрать фильмы
    - сохранить фильмы
    - обновить сеансы через session_parser
    """

    def __init__(
        self,
        movie_repo: MovieRepository,
        cinema_repo: CinemaRepository,
        session_repo: SessionRepository,
        cinema_movie_repo: CinemaMovieRepository,
        main_parser: KinomaxMainPageParser,
        session_parser: KinomaxSessionParser,
        movie_detail_parser: MovieDetailParser,
    ):
        self.movie_repo = movie_repo
        self.cinema_repo = cinema_repo
        self.session_repo = session_repo
        self.cinema_movie_repo = cinema_movie_repo
        self.main_parser = main_parser
        self.session_parser = session_parser
        self.movie_detail_parser = movie_detail_parser

    # ==========================================================
    # CINEMA ID
    # ==========================================================

    def _get_kinomax_cinema_id(self) -> int:
        cinema = self.cinema_repo.get_by_name("КИНОМАКС")

        if cinema:
            return cinema.id

        raise RuntimeError("Кинотеатр 'КИНОМАКС' не найден в БД. Пожалуйста, выполните миграции алембика.")

    # ==========================================================
    # CITY SELECT
    # ==========================================================

    def _select_city_once(self, city: str):
        logger.info(f"Выбор города: {city}")

        self.main_parser.wait_for_element(By.TAG_NAME, "body")

        # кнопка "Нет" в модалке
        no_button_xpath = kinomax_settings.CITY_SELECTORS[
            "no_button_xpath"
        ].format(
            text=kinomax_settings.CITY_MODAL["no_button_text"]
        )

        self.main_parser.click(By.XPATH, no_button_xpath)
        self.main_parser.sleep(1)

        # кнопка нужного города
        city_xpath = kinomax_settings.CITY_SELECTORS[
            "city_button_xpath"
        ].format(city=city)

        self.main_parser.click(By.XPATH, city_xpath)
        self.main_parser.sleep(2)

    # ==========================================================
    # MAIN FLOW
    # ==========================================================

    def run(self, city: str = "Липецк"):
        """
        Главный публичный метод.
        """

        logger.info("=== Запуск парсинга КИНОМАКС ===")

        cinema_id = self._get_kinomax_cinema_id()

        # 1️⃣ Открываем сайт
        self.main_parser.navigate(kinomax_settings.KINOMAX_URL)

        # 2️⃣ Выбираем город (1 раз)
        self._select_city_once(city)

        # 3️⃣ Получаем фильмы
        films = self.main_parser.parse_all_movies()

        if not films:
            logger.warning("Фильмы не найдены")
            return

        logger.info(f"Найдено фильмов: {len(films)}")

        # 4️⃣ Обрабатываем каждый фильм
        for index, film_data in enumerate(films, 1):
            try:
                self._process_single_movie(
                    film_data=film_data,
                    cinema_id=cinema_id,
                    index=index,
                    total=len(films),
                )
            except Exception:
                logger.exception(
                    f"Ошибка обработки фильма #{index}"
                )

        logger.info("=== Парсинг КИНОМАКС завершён ===")

    # ==========================================================
    # MOVIE PROCESSING
    # ==========================================================

    def _process_single_movie(
        self,
        film_data: dict,
        cinema_id: int,
        index: int,
        total: int,
    ):
        title = film_data.get("title")
        url = film_data.get("url")

        if not title or not url:
            logger.warning(
                f"[{index}/{total}] Пропуск — нет title или url"
            )
            return

        logger.info(f"[{index}/{total}] Обработка: {title}")

        # 1️⃣ Получаем детали фильма
        details = self.movie_detail_parser.parse_by_title(title)

        if not details:
            logger.warning(f"Детали не получены → {title}")
            return

        kinomax_id = extract_kinomax_id(url)

        # 2️⃣ Сохраняем / получаем фильм
        movie = self.movie_repo.get_or_create(
            name=details.title,
            cinema_id=cinema_id,
            defaults={
                "description": details.description,
                "genre": ", ".join(details.genres),
                "poster": details.poster_url,
                "kinopoisk_id": details.kinopoisk_id,
                "additional_data": details.additional_data,
            },
        )

        logger.info(
            f"Фильм сохранён: {movie.name} (id={movie.id})"
        )

        # 2️⃣a Обновляем связь фильм-кинотеатр с cinema-specific данными
        cinema_movie = self.cinema_movie_repo.get_by_cinema_and_movie(
            cinema_id=cinema_id,
            movie_id=movie.id
        )
        
        if cinema_movie and (not cinema_movie.cinema_movie_id or not cinema_movie.cinema_movie_url):
            # Обновляем существующую связь с cinema-specific данными
            self.cinema_movie_repo.update(
                cinema_id=cinema_id,
                movie_id=movie.id,
                data={
                    "cinema_movie_id": kinomax_id,
                    "cinema_movie_url": url,
                }
            )
            logger.info(f"✓ Связь фильм-кинотеатр обновлена: cinema_movie_id={kinomax_id}")

        # 3️⃣ Обновляем сеансы
        self._update_sessions(
            movie_id_kinomax=kinomax_id,
            movie_db_id=movie.id,
            cinema_id=cinema_id,
            movie_title=movie.name,
        )

    # ==========================================================
    # SESSIONS
    # ==========================================================

    def _update_sessions(
        self,
        movie_id_kinomax: str,
        movie_db_id: int,
        cinema_id: int,
        movie_title: str,
    ):
        logger.info(f"Обновление сеансов: {movie_title}")

        sessions = self.session_parser.parse_sessions(
            movie_id=movie_id_kinomax,
            movie_db_id=movie_db_id,
            cinema_id=cinema_id,
            days=5,
        )

        if not sessions:
            logger.warning(
                f"Сеансы не найдены: {movie_title}"
            )
            return

        for session in sessions:
            self.session_repo.get_or_create(
                defaults={
                    "session_id": session.session_id,
                    "movie_id": session.movie_id,
                    "cinema_id": session.cinema_id,
                    "date": session.date,
                    "updated_at": session.updated_at,
                }
            )

        logger.info(
            f"Сохранено {len(sessions)} сеансов: {movie_title}"
        )
