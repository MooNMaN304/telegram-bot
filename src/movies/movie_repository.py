from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from sqlalchemy import Integer, and_
from .movie_model import MovieModel
from datetime import date
from src.sessions.session_model import SessionModel
from sqlalchemy import func

class MovieRepository:
    def __init__(self, session: Session, movie_model: type[MovieModel], session_model: SessionModel):
        self.db = session
        self.movie_model = movie_model
        self.session_model = session_model
    
    def get_all(self) -> List[MovieModel]:
        return self.db.query(self.movie_model).all()
    
    def get_by_id(self, movie_id: int) -> Optional[MovieModel]:
        return self.db.query(self.movie_model).filter(self.movie_model.id == movie_id).first()
    
    def create(self, movie_data: dict) -> MovieModel:
        # Обработка related_movies при создании
        if 'related_movies' in movie_data and movie_data['related_movies'] is None:
            movie_data['related_movies'] = {}
            
        movie = self.movie_model(**movie_data)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie
    
    def update(self, movie_id: int, movie_data: dict) -> Optional[MovieModel]:
        movie = self.get_by_id(movie_id)
        if movie:
            # Обработка related_movies при обновлении
            if 'related_movies' in movie_data and movie_data['related_movies'] is None:
                movie_data['related_movies'] = {}
                
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
    
    def get_by_external_id(self, cinema_id: int, external_id_key: str, external_id_value: int) -> Optional[MovieModel]:
        """
        Получить фильм по внешнему ID (например, id_malibu), хранящемуся в additional_data.
        """
        return (
            self.db.query(self.movie_model)
            .filter(
                self.movie_model.cinema_id == cinema_id,
                self.movie_model.additional_data[external_id_key].astext.cast(Integer) == external_id_value
            )
            .first()
        )
    
    def get_by_genre(self, genre: str) -> List[MovieModel]:
        return self.db.query(self.movie_model).filter(self.movie_model.genre.ilike(f"%{genre}%")).all()
    
    def search_by_name(self, name: str) -> List[MovieModel]:
        return self.db.query(self.movie_model).filter(self.movie_model.name.ilike(f"%{name}%")).all()
    
    def get_or_create(self, name: str, cinema_id: int, defaults: dict = None) -> MovieModel:
        """
        Проверяет, есть ли фильм с таким названием и кинотеатром.
        Если нет — создаёт новый.
        
        :param name: название фильма
        :param cinema_id: ID кинотеатра
        :param defaults: дополнительные данные для создания фильма
        :return: объект MovieModel
        """
        movie = (
            self.db.query(self.movie_model)
            .filter(self.movie_model.name == name, self.movie_model.cinema_id == cinema_id)
            .first()
        )

        if movie:
            return movie

        create_data = {"name": name, "cinema_id": cinema_id}
        if defaults:
            create_data.update(defaults)
        
        # Инициализируем related_movies пустым словарем, если не передано
        if 'related_movies' not in create_data:
            create_data['related_movies'] = {}
            
        return self.create(create_data)
    
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
    def get_sessions_by_movie_and_date(self, movie_id: int, session_date: date) -> list[SessionModel]:
        return (
            self.db.query(self.session_model)
            .filter(
                self.session_model.movie_id == movie_id,
                func.date(self.session_model.date) == session_date
            )
            .all()
        )
