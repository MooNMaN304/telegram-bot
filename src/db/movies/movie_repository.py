from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from sqlalchemy import Integer, and_
from .movie_model import MovieModel
from datetime import date
from src.db.sessions.session_model import SessionModel
from src.db.cinema_movie.cinema_movie_model import CinemaMovieModel
from sqlalchemy import func

from src.utils.logger import get_logger

logger = get_logger(__name__)


class MovieRepository:
    def __init__(
        self,
        session: Session,
        movie_model: type[MovieModel],
        session_model: type[SessionModel],
        cinema_movie_model: type[CinemaMovieModel],
    ):
        self.db = session
        self.movie_model = movie_model
        self.session_model = session_model
        self.cinema_movie_model = cinema_movie_model

    def get_all(self) -> List[MovieModel]:
        return self.db.query(self.movie_model).all()

    def get_by_id(self, movie_id: int) -> Optional[MovieModel]:
        return self.db.query(self.movie_model).filter(self.movie_model.id == movie_id).first()

    def create(self, movie_data: dict) -> MovieModel:
        # Удаляем cinema_id, так как он больше не нужен в MovieModel
        movie_data.pop("cinema_id", None)

        movie = self.movie_model(**movie_data)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def update(self, movie_id: int, movie_data: dict) -> Optional[MovieModel]:
        movie = self.get_by_id(movie_id)
        if movie:
            # Удаляем cinema_id, так как он больше не нужен в MovieModel
            movie_data.pop("cinema_id", None)

            for key, value in movie_data.items():
                setattr(movie, key, value)
            self.db.commit()
            self.db.refresh(movie)
            return movie
        return None

    def delete(self, movie_id: int) -> bool:
        movie = self.get_by_id(movie_id)
        if movie:
            self.db.delete(movie)
            self.db.commit()
            return True
        return False

    def get_by_external_id(
        self, cinema_id: int, external_id_key: str, external_id_value: int
    ) -> Optional[MovieModel]:
        """
        Получить фильм по внешнему ID (например, id_malibu), хранящемуся в additional_data.
        Фильтруется по кинотеатру через CinemaMovieModel.
        """
        return (
            self.db.query(self.movie_model)
            .join(CinemaMovieModel, CinemaMovieModel.movie_id == self.movie_model.id)
            .filter(
                CinemaMovieModel.cinema_id == cinema_id,
                self.movie_model.additional_data[external_id_key].astext.cast(Integer)
                == external_id_value,
            )
            .first()
        )

    def get_by_genre(self, genre: str) -> List[MovieModel]:
        return (
            self.db.query(self.movie_model).filter(self.movie_model.genre.ilike(f"%{genre}%")).all()
        )

    def search_by_name(self, name: str) -> List[MovieModel]:
        return (
            self.db.query(self.movie_model).filter(self.movie_model.name.ilike(f"%{name}%")).all()
        )

    def get_or_create(self, name: str, cinema_id: int, defaults: dict = None) -> MovieModel:
        """
        Получает фильм по названию или создаёт новый.
        Автоматически создаёт связь в CinemaMovieModel.

        :param name: название фильма
        :param cinema_id: ID кинотеатра
        :param defaults: дополнительные данные для создания фильма
                 - должен содержать additional_data (инфо из kinopoisk)
        :return: объект MovieModel
        """
        # 1️⃣ Проверяем есть ли уже такой фильм (по названию)
        movie = self.db.query(self.movie_model).filter(
            self.movie_model.name == name
        ).first()

        if movie:
            # Проверяем есть ли уже связь с этим кинотеатром
            existing_relation = (
                self.db.query(CinemaMovieModel)
                .filter(
                    CinemaMovieModel.movie_id == movie.id,
                    CinemaMovieModel.cinema_id == cinema_id
                )
                .first()
            )
            
            if not existing_relation:
                # Создаём новую связь
                self._create_cinema_movie_relation(movie.id, cinema_id)
            
            return movie

        # 2️⃣ Если не нашли по названию — проверяем по kinopoisk_id
        #    (избегаем UniqueViolation, когда фильм уже есть, но с другим названием)
        kinopoisk_id = defaults.get("kinopoisk_id") if defaults else None
        if kinopoisk_id is not None:
            movie_by_kp = self.db.query(self.movie_model).filter(
                self.movie_model.kinopoisk_id == kinopoisk_id
            ).first()

            if movie_by_kp:
                # Фильм уже существует с другим названием — обновляем название
                # и добавляем связь с кинотеатром
                logger.info(
                    "Фильм с kinopoisk_id=%s найден под названием '%s', "
                    "обновляем на '%s'",
                    kinopoisk_id, movie_by_kp.name, name,
                )
                self.update(movie_by_kp.id, {"name": name})

                # Проверяем связь с кинотеатром
                existing_relation = (
                    self.db.query(CinemaMovieModel)
                    .filter(
                        CinemaMovieModel.movie_id == movie_by_kp.id,
                        CinemaMovieModel.cinema_id == cinema_id
                    )
                    .first()
                )
                if not existing_relation:
                    self._create_cinema_movie_relation(movie_by_kp.id, cinema_id)

                return movie_by_kp

        # 3️⃣ Создаём новый фильм
        create_data = {"name": name}
        if defaults:
            create_data.update(defaults)

        # Инициализируем поля если их нет
        if "additional_data" not in create_data:
            create_data["additional_data"] = {}

        # Создаём фильм без cinema_id
        movie = self.create(create_data)

        # Создаём связь с кинотеатром
        self._create_cinema_movie_relation(movie.id, cinema_id)

        return movie

    def _create_cinema_movie_relation(self, movie_id: int, cinema_id: int) -> CinemaMovieModel:
        """
        Создаёт связь между кинотеатром и фильмом.
        
        :param movie_id: ID фильма
        :param cinema_id: ID кинотеатра
        :return: объект CinemaMovieModel
        """
        relation = CinemaMovieModel(movie_id=movie_id, cinema_id=cinema_id)
        self.db.add(relation)
        self.db.commit()
        self.db.refresh(relation)
        return relation

    # фильмы с сеансами на сегодня
    def get_movies_with_sessions_today(self) -> List[MovieModel]:
        """
        Получает список фильмов, у которых есть сеансы на сегодня.
        Использует подзапрос для обхода проблемы DISTINCT с JSON полями в PostgreSQL.
        """
        today = date.today()
        # Подзапрос для получения уникальных ID фильмов с сеансами на сегодня
        # Это обходит проблему "could not identify an equality operator for type json"
        return (
            self.db.query(self.movie_model)
            .filter(
                self.movie_model.id.in_(
                    self.db.query(self.session_model.movie_id)
                    .filter(func.date(self.session_model.date) == today)
                    .distinct()
                )
            )
            .all()
        )

    def get_movies_by_cinema(self, cinema_id: int) -> List[MovieModel]:
        """
        Получает все фильмы, которые идут в конкретном кинотеатре.
        DEPRECATED: Использовать CinemaMovieRepository.get_movies_by_cinema() вместо этого.
        """
        return (
            self.db.query(self.movie_model)
            .join(self.cinema_movie_model)
            .filter(self.cinema_movie_model.cinema_id == cinema_id)
            .all()
        )

