import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.db.database import SessionLocal
from src.movies.movie_repository import MovieRepository
from src.movies.movie_model import MovieModel
from src.cinemas.cinema_repository import CinemaRepository
from src.cinemas.cinema_model import CinemaModel
from src.sessions.session_repository import SessionRepository
from src.sessions.session_model import SessionModel

from src.parsing_movie.malibu_cinema.extractor import (
    MalibuMainPageExtractor, 
    MalibuDetailsExtractor,
)
from src.parsing_movie.malibu_cinema.session_extractor import MalibuSessionExtractor
from src.parsing_movie.malibu_cinema.main_page_parser import MalibuMainPageParser
from src.parsing_movie.malibu_cinema.details_parser import MalibuDetailsParser
from src.parsing_movie.malibu_cinema.session_parser import MalibuSessionParser
from src.parsing_movie.malibu_cinema.service import MalibuService
from src.parsing_movie.malibu_cinema.malibu_settings import malibu_settings
from src.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    db: Session | None = None
    try:
        db = SessionLocal()

        # Репозитории
        movie_repo = MovieRepository(session=db, movie_model=MovieModel)
        cinema_repo = CinemaRepository(db=db, cinema_model=CinemaModel)
        session_repo = SessionRepository(db=db, session_model=SessionModel)

        # --- Extractors ---
        main_extractor = MalibuMainPageExtractor(selectors=malibu_settings.CINEMA_SELECTORS["malibu"])
        details_extractor = MalibuDetailsExtractor(selectors=malibu_settings.MOVIE_DETAILS_SELECTORS["malibu"])
        session_extractor = MalibuSessionExtractor(selectors=malibu_settings.SESSION_SELECTORS["malibu"])

        # --- Парсеры ---
        main_parser = MalibuMainPageParser(
            url=malibu_settings.MALIBU_URL,
            css_selector=malibu_settings.CINEMA_SELECTORS["malibu"],
            wait_time=settings.WAIT_PAGE_LOAD,
            extractor=main_extractor
        )

        details_parser = MalibuDetailsParser(
            extractor=details_extractor,
            driver=main_parser.driver
        )

        session_parser = MalibuSessionParser(
            extractor=session_extractor
        )

        # --- Сервис ---
        malibu_service = MalibuService(
            db=db,
            movie_repo=movie_repo,
            cinema_repo=cinema_repo,
            session_repo=session_repo,
            main_parser=main_parser,
            details_parser=details_parser,
            session_parser=session_parser
        )

        # --- Основной запуск ---
        malibu_cinema_id = malibu_service.get_malibu_cinema_id()
        malibu_service.malibu_movies_record(malibu_cinema_id)

        logger.info("✅ Парсинг фильмов и расписания Малибу успешно завершён")

    except SQLAlchemyError as e:
        logger.error(f"Ошибка работы с базой данных: {e}")
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка в main(): {e}")
    finally:
        if db:
            db.close()
        # Закрываем драйвер
        if 'main_parser' in locals() and hasattr(main_parser, 'driver'):
            main_parser.driver.quit()


if __name__ == "__main__":
    main()