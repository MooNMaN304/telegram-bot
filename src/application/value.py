from src.db.database import get_session

from src.movies.movie_repository import MovieRepository
from src.movies.movie_model import MovieModel
from src.cinemas.cinema_repository import CinemaRepository
from src.cinemas.cinema_model import CinemaModel
from src.sessions.session_repository import SessionRepository
from src.sessions.session_model import SessionModel
from src.user.user_model import UserModel
from src.user.user_repository import UserRepository

from src.parsing_movie.malibu_cinema.extractor import MalibuMainPageExtractor, MalibuDetailsExtractor
from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor
from src.parsing_movie.malibu_cinema.main_page_parser import MalibuMainPageParser
from src.parsing_movie.malibu_cinema.details_parser import MalibuDetailsParser
from src.parsing_movie.malibu_cinema.session_parser import MalibuSessionParser
from src.parsing_movie.malibu_cinema.service import MalibuService
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings
from src.user.user_service import UserService

from src.settings import settings

session = get_session()

# --- Репозитории ---
def get_movie_repository():
    return MovieRepository(session=session, movie_model=MovieModel, session_model=SessionModel)

def get_cinema_repository():
    return CinemaRepository(session=session, cinema_model=CinemaModel)

def get_session_repository():
    return SessionRepository(session=session, session_model=SessionModel)

def get_user_repository():
    return UserRepository(session=session, user_model=UserModel)


# --- Extractors ---
def get_main_extractor():
    return MalibuMainPageExtractor(selectors=malibu_settings.CINEMA_SELECTORS["malibu"])

def get_details_extractor():
    return MalibuDetailsExtractor(selectors=malibu_settings.MOVIE_DETAILS_SELECTORS["malibu"])

def get_session_extractor():
    return MalibuSessionExtractor(selectors=malibu_settings.SESSION_SELECTORS["malibu"])


# --- Parsers ---
def get_main_parser():
    return MalibuMainPageParser(
        url=malibu_settings.MALIBU_URL,
        css_selector=malibu_settings.CINEMA_SELECTORS["malibu"],
        wait_time=settings.WAIT_PAGE_LOAD,
        extractor=get_main_extractor()
    )

def get_details_parser(main_parser):
    return MalibuDetailsParser(
        extractor=get_details_extractor(),
        driver=main_parser.driver
    )

def get_session_parser():
    return MalibuSessionParser(extractor=get_session_extractor())


# --- Сервисы ---
def get_malibu_service():
    main_parser = get_main_parser()
    details_parser = get_details_parser(main_parser)
    session_parser = get_session_parser()

    movie_repo = get_movie_repository()
    cinema_repo = get_cinema_repository()
    session_repo = get_session_repository()

    return MalibuService(
        movie_repo=movie_repo,
        cinema_repo=cinema_repo,
        session_repo=session_repo,
        main_parser=main_parser,
        details_parser=details_parser,
        session_parser=session_parser
    )

def get_user_service():
    user_repo = get_user_repository()
    return UserService(user_repo=user_repo)
