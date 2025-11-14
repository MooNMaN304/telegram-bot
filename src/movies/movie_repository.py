from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import Integer
from .movie_model import MovieModel

class MovieRepository:
    def __init__(self, db: Session, movie_model: type[MovieModel]):
        self.db = db
        self.movie_model = movie_model
    
    def get_all(self) -> List[MovieModel]:
        return self.db.query(self.movie_model).all()
    
    def get_by_id(self, movie_id: int) -> Optional[MovieModel]:
        return self.db.query(self.movie_model).filter(self.movie_model.id == movie_id).first()
    
    def create(self, movie_data: dict) -> MovieModel:
        movie = self.movie_model(**movie_data)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie
    
    def update(self, movie_id: int, movie_data: dict) -> Optional[MovieModel]:
        movie = self.get_by_id(movie_id)
        if movie:
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
        return self.db.query(self.movie_model).filter(self.movie_model.genre == genre).all()
    
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
        
        return self.create(create_data)
