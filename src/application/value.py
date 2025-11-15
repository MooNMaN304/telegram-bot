# Здесь собирать обьекты как в FastAPI
# SERVICE
# REPO
# Что-то еще
# src/application/parser_factory.py
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

from src.parsing_movie.malibu_cinema.extractor import (
    MalibuMainPageExtractor,
    MalibuDetailsExtractor,
)
from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor
from src.parsing_movie.malibu_cinema.main_page_parser import MalibuMainPageParser
from src.parsing_movie.malibu_cinema.details_parser import MalibuDetailsParser
from src.parsing_movie.malibu_cinema.session_parser import MalibuSessionParser
from src.parsing_movie.malibu_cinema.service import MalibuService
from src.settings import settings


# сборка репозиториев
def create_movie_repository(db: Session, movie_model: MovieModel) -> MovieRepository:
    return MovieRepository(db=db, movie_model=movie_model)

def create_cinema_repository(db: Session) -> CinemaRepository:
    return CinemaRepository(db=db, cinema_model=CinemaModel)

def create_session_repository(db: Session) -> SessionRepository:
    return SessionRepository(db=db, session_model=SessionModel)

def create_user_repository(db: Session):
    return UserRepository(db=db, user_model=UserModel)


# сборка экстракторов
def create_main_page_extractor() -> MalibuMainPageExtractor:
    return MalibuMainPageExtractor(selectors=settings.CINEMA_SELECTORS["malibu"])

def create_details_extractor() -> MalibuDetailsExtractor:
    return MalibuDetailsExtractor(selectors=settings.MOVIE_DETAILS_SELECTORS["malibu"])

def create_session_extractor() -> MalibuSessionExtractor:
    return MalibuSessionExtractor(selectors=settings.SESSION_SELECTORS["malibu"])

# сборка сервиса
def create_main_parser() -> MalibuMainPageParser:
    extractor = create_main_page_extractor()
    return MalibuMainPageParser(
        url=settings.MALIBU_URL,
        css_selector=settings.CINEMA_SELECTORS["malibu"],
        wait_time=settings.WAIT_PAGE_LOAD,
        extractor=extractor
    )

def create_details_parser(main_parser: MalibuMainPageParser) -> MalibuDetailsParser:
    extractor = create_details_extractor()
    return MalibuDetailsParser(
        extractor=extractor,
        driver=main_parser.driver
    )

def create_session_parser() -> MalibuSessionParser:
    extractor = create_session_extractor()
    return MalibuSessionParser(
        extractor=extractor
    )

def create_malibu_service() -> MalibuService:
    """Собирает и возвращает полностью готовый MalibuService"""
    db: Session = SessionLocal()

    # Репозитории
    movie_repo = create_movie_repository(db=db, movie_model=MovieModel)
    cinema_repo = create_cinema_repository(db=db)
    session_repo = create_session_repository(db=db)

    # Парсеры
    main_parser = create_main_parser()
    details_parser = create_details_parser(main_parser=main_parser)
    session_parser = create_session_parser()

    # Сервис
    service = MalibuService(
        db=db,
        movie_repo=movie_repo,
        cinema_repo=cinema_repo,
        session_repo=session_repo,
        main_parser=main_parser,
        details_parser=details_parser,
        session_parser=session_parser
    )

    return service
