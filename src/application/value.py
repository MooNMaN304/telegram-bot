from sqlalchemy.orm import Session
from src.db.database import SessionLocal

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


# --- База ---
def get_session() -> Session:
    return SessionLocal()


# --- Репозитории ---
def get_movie_repository(session: Session):
    return MovieRepository(session=session, movie_model=MovieModel)

def get_cinema_repository(db: Session):
    return CinemaRepository(db=db, cinema_model=CinemaModel)

def get_session_repository(db: Session):
    return SessionRepository(db=db, session_model=SessionModel)

def get_user_repository(db: Session):
    return UserRepository(db=db, user_model=UserModel)


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
    db = get_session()

    main_parser = get_main_parser()

    service = MalibuService(
        db=db,
        movie_repo=get_movie_repository(db),
        cinema_repo=get_cinema_repository(db),
        session_repo=get_session_repository(db),
        main_parser=main_parser,
        details_parser=get_details_parser(main_parser),
        session_parser=get_session_parser()
    )
    return service

def get_user_service() -> UserService:
    db = get_session()
    user_repo = get_user_repository(db)
    return UserService(user_repo=user_repo)
