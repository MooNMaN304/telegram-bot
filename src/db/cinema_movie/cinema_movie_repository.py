from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from sqlalchemy import func
from .cinema_movie_model import CinemaMovieModel


class CinemaMovieRepository:
    """Репозиторий для работы с связями фильм-кинотеатр"""
    
    def __init__(
        self, 
        session: Session, 
        cinema_movie_model: type[CinemaMovieModel],
        session_model=None,  # Импортируется для JOIN операций
        movie_model=None,    # Импортируется для JOIN операций
    ):
        self.db = session
        self.cinema_movie_model = cinema_movie_model
        self.session_model = session_model
        self.movie_model = movie_model

    def get_or_create(
        self,
        cinema_id: int,
        movie_id: int,
        defaults: dict = None
    ) -> CinemaMovieModel:
        """Получить или создать связь фильм-кинотеатр"""
        cinema_movie = self.db.query(self.cinema_movie_model).filter(
            self.cinema_movie_model.cinema_id == cinema_id,
            self.cinema_movie_model.movie_id == movie_id,
        ).first()

        if cinema_movie:
            return cinema_movie

        # Создаём новую связь
        cinema_movie = self.cinema_movie_model(
            cinema_id=cinema_id,
            movie_id=movie_id,
            **(defaults or {})
        )
        self.db.add(cinema_movie)
        self.db.commit()
        self.db.refresh(cinema_movie)
        return cinema_movie

    def get_by_cinema_and_movie(
        self,
        cinema_id: int,
        movie_id: int
    ) -> Optional[CinemaMovieModel]:
        """Получить связь по cinema_id и movie_id"""
        return self.db.query(self.cinema_movie_model).filter(
            self.cinema_movie_model.cinema_id == cinema_id,
            self.cinema_movie_model.movie_id == movie_id,
        ).first()

    def get_movies_by_cinema(self, cinema_id: int) -> List[CinemaMovieModel]:
        """Получить все фильмы в кинотеатре"""
        return self.db.query(self.cinema_movie_model).filter(
            self.cinema_movie_model.cinema_id == cinema_id
        ).all()

    def get_cinemas_by_movie(self, movie_id: int) -> List[CinemaMovieModel]:
        """Получить все кинотеатры, где идёт фильм"""
        return self.db.query(self.cinema_movie_model).filter(
            self.cinema_movie_model.movie_id == movie_id
        ).all()

    def get_movies_by_cinema_today(self, cinema_id: int, target_date: date = None) -> List:
        """
        Получить все фильмы в кинотеатре на конкретную дату с сеансами.
        Возвращает объекты фильмов, связанные с этим кинотеатром.
        """
        if target_date is None:
            target_date = date.today()
        
        # Требуется session_model и movie_model для JOIN
        if not self.session_model or not self.movie_model:
            raise ValueError("session_model и movie_model должны быть переданы в конструктор")
        
        return (
            self.db.query(self.movie_model)
            .join(self.cinema_movie_model, self.movie_model.id == self.cinema_movie_model.movie_id)
            .join(self.session_model, self.movie_model.id == self.session_model.movie_id)
            .filter(
                self.cinema_movie_model.cinema_id == cinema_id,
                func.date(self.session_model.date) == target_date
            )
            .distinct(self.movie_model.id)
            .all()
        )

    def get_cinemas_by_movie_today(self, movie_id: int, target_date: date = None) -> List:
        """
        Получить все кинотеатры, где идёт фильм на конкретную дату с сеансами.
        Возвращает объекты кинотеатров, где показывается этот фильм.
        """
        if target_date is None:
            target_date = date.today()
        
        # Требуется session_model и cinema_model для JOIN
        if not self.session_model:
            raise ValueError("session_model должна быть передана в конструктор")
        
        from src.db.cinemas.cinema_model import CinemaModel
        
        return (
            self.db.query(CinemaModel)
            .join(self.cinema_movie_model, CinemaModel.id == self.cinema_movie_model.cinema_id)
            .join(self.session_model, self.session_model.movie_id == self.cinema_movie_model.movie_id)
            .filter(
                self.cinema_movie_model.movie_id == movie_id,
                func.date(self.session_model.date) == target_date,
                self.session_model.cinema_id == self.cinema_movie_model.cinema_id,
            )
            .distinct(CinemaModel.id)
            .all()
        )

    def update(
        self,
        cinema_id: int,
        movie_id: int,
        data: dict
    ) -> Optional[CinemaMovieModel]:
        """Обновить данные связи"""
        cinema_movie = self.get_by_cinema_and_movie(cinema_id, movie_id)
        
        if cinema_movie:
            for key, value in data.items():
                if hasattr(cinema_movie, key):
                    setattr(cinema_movie, key, value)
            self.db.commit()
            self.db.refresh(cinema_movie)
            return cinema_movie
        
        return None

    def delete(self, cinema_id: int, movie_id: int) -> bool:
        """Удалить связь"""
        cinema_movie = self.get_by_cinema_and_movie(cinema_id, movie_id)
        
        if cinema_movie:
            self.db.delete(cinema_movie)
            self.db.commit()
            return True
        
        return False
