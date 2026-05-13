from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from sqlalchemy import Integer, and_
from .movie_model import MovieModel
from datetime import date
from src.db.sessions.session_model import SessionModel
from src.db.cinema_movie.cinema_movie_model import CinemaMovieModel
from sqlalchemy import func


class MovieRepository:
    def __init__(
        self, session: Session, movie_model: type[MovieModel], session_model: SessionModel
    ):
        self.db = session
        self.movie_model = movie_model
        self.session_model = session_model

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
        # Проверяем есть ли уже такой фильм (по названию)
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

        # Создаём новый фильм
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
    def get_movies_with_sessions_today(self):
        today = date.today()
        return (
            self.db.query(self.movie_model)
            .join(self.session_model)
            .filter(func.date(self.session_model.date) == today)
            .all()
        )

    # сеансы фильма по дате
    def get_sessions_by_movie_and_date(
        self, movie_id: int, session_date: date
    ) -> list[SessionModel]:
        return (
            self.db.query(self.session_model)
            .filter(
                self.session_model.movie_id == movie_id,
                func.date(self.session_model.date) == session_date,
            )
            .all()
        )
