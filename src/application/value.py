"""Factory functions for creating repositories, parsers, and controllers.

IMPORTANT: Each function creates its own DB session via get_session().
Previously, a module-level `session = get_session()` was used, which caused
stale sessions in long-running Celery workers. Now every call gets a fresh session.
"""

from src.db.database import get_session

from src.db.movies.movie_repository import MovieRepository
from src.db.movies.movie_model import MovieModel
from src.db.cinemas.cinema_repository import CinemaRepository
from src.db.cinemas.cinema_model import CinemaModel
from src.db.sessions.session_repository import SessionRepository
from src.db.sessions.session_model import SessionModel
from src.db.sessions.gigachat_response_schema import GigaChatScheduleResponse
from src.db.cinema_movie.cinema_movie_repository import CinemaMovieRepository
from src.db.cinema_movie.cinema_movie_model import CinemaMovieModel
from src.db.user.user_model import UserModel
from src.db.user.user_repository import UserRepository
from src.db.user.user_service import UserService
from src.db.movies.movie_service import MovieService

from src.utils.kino_api.client import KinoAPIClient
from src.utils.movie_detail_parser import MovieDetailParser
from src.utils.gigachat_request import GigaChatScheduleParser

from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings

from src.settings import settings


# --- Вспомогательные функции ---
def _resolve_gigachat_credentials():
    """Получить credentials для GigaChat из настроек"""
    return settings.GIGACHAT_API_KEY


# --- Репозитории ---
def get_movie_repository():
    session = get_session()
    return MovieRepository(
        session=session,
        movie_model=MovieModel,
        session_model=SessionModel,
        cinema_movie_model=CinemaMovieModel,
    )


def get_cinema_repository():
    session = get_session()
    return CinemaRepository(session=session, cinema_model=CinemaModel)


def get_session_repository():
    session = get_session()
    return SessionRepository(session=session, session_model=SessionModel)


def get_cinema_movie_repository():
    session = get_session()
    return CinemaMovieRepository(
        session=session,
        cinema_movie_model=CinemaMovieModel,
        session_model=SessionModel,
        movie_model=MovieModel,
    )


def get_user_repository():
    session = get_session()
    return UserRepository(session=session, user_model=UserModel)


# --- Extractors ---
def get_session_extractor():
    return MalibuSessionExtractor(malibu_settings.SESSION_SELECTORS["malibu"])


def get_main_parser(driver=None):
    """Parser инициализирует extractor сам."""
    from src.parsing_movie.malibu_cinema.main_page_parser import MalibuMainPageParser
    return MalibuMainPageParser(driver=driver, wait_time=settings.WAIT_PAGE_LOAD)


def get_movie_detail_parser(driver=None):
    api_client = KinoAPIClient()
    return MovieDetailParser(api_client=api_client)


def get_session_parser(driver=None):
    from src.parsing_movie.malibu_cinema.session_parser import MalibuSessionParser
    return MalibuSessionParser(
        driver=driver,
        wait_time=settings.WAIT_PAGE_LOAD,
    )


# --- Сервисы ---
def get_malibu_controller(driver=None):
    from src.parsing_movie.malibu_cinema.controller import MalibuController
    return MalibuController(
        movie_repo=get_movie_repository(),
        cinema_repo=get_cinema_repository(),
        session_repo=get_session_repository(),
        cinema_movie_repo=get_cinema_movie_repository(),
        main_parser=get_main_parser(driver=driver),
        movie_detail_parser=get_movie_detail_parser(driver=driver),
        session_parser=get_session_parser(driver=driver),
    )

def build_kinomax_controller(driver=None):
    from src.parsing_movie.kinomax_cinema.controller import KinomaxController
    session = get_session()

    # =========================
    # REPOSITORIES
    # =========================
    movie_repo = MovieRepository(
        session=session,
        movie_model=MovieModel,
        session_model=SessionModel,
        cinema_movie_model=CinemaMovieModel,
    )

    cinema_repo = CinemaRepository(
        session=session,
        cinema_model=CinemaModel,
    )

    session_repo = SessionRepository(
        session=session,
        session_model=SessionModel,
    )

    cinema_movie_repo = CinemaMovieRepository(
        session=session,
        cinema_movie_model=CinemaMovieModel,
        session_model=SessionModel,
        movie_model=MovieModel,
    )

    # =========================
    # PARSERS
    # =========================
    from src.parsing_movie.kinomax_cinema.main_page_parser import KinomaxMainPageParser
    main_parser = KinomaxMainPageParser(
        driver=driver,
        wait_time=settings.WAIT_PAGE_LOAD,
    )

    gigachat_parser = GigaChatScheduleParser(
        credentials=_resolve_gigachat_credentials(),
        response_schema=GigaChatScheduleResponse,
        model="GigaChat",
        temperature=0.1,
        max_retries=3,
    )

    from src.parsing_movie.kinomax_cinema.session_parser import KinomaxSessionParser
    session_parser = KinomaxSessionParser(
        driver=driver,
        gigachat_parser=gigachat_parser,
        wait_time=settings.WAIT_PAGE_LOAD,
    )

    movie_detail_parser = MovieDetailParser(
        api_client=KinoAPIClient()
    )

    # =========================
    # CONTROLLER
    # =========================
    return KinomaxController(
        movie_repo=movie_repo,
        cinema_repo=cinema_repo,
        session_repo=session_repo,
        cinema_movie_repo=cinema_movie_repo,
        main_parser=main_parser,
        session_parser=session_parser,
        movie_detail_parser=movie_detail_parser,
    )

def get_user_service():
    user_repo = get_user_repository()
    return UserService(user_repo=user_repo)


def get_movie_service():
    return MovieService(
        movie_repo=get_movie_repository(),
        session_repo=get_session_repository(),
        cinema_movie_repo=get_cinema_movie_repository(),
    )
