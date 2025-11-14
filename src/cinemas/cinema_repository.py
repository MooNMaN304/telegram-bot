from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from .cinema_model import CinemaModel

class CinemaRepository:
    def __init__(self, db: Session, cinema_model: type[CinemaModel]):
        self.db = db
        self.cinema_model = cinema_model
    
    def get_all(self) -> List[CinemaModel]:
        """Получить все кинотеатры"""
        return self.db.query(self.cinema_model).all()
    
    def get_by_id(self, cinema_id: int) -> Optional[CinemaModel]:
        """Получить кинотеатр по ID"""
        return self.db.query(self.cinema_model).filter(self.cinema_model.id == cinema_id).first()
    
    def create(self, cinema_data: dict) -> CinemaModel:
        """Создать новый кинотеатр"""
        cinema = self.cinema_model(**cinema_data)
        self.db.add(cinema)
        self.db.commit()
        self.db.refresh(cinema)
        return cinema
    
    def update(self, cinema_id: int, cinema_data: dict) -> Optional[CinemaModel]:
        """Обновить кинотеатр"""
        cinema = self.get_by_id(cinema_id)
        if cinema:
            for key, value in cinema_data.items():
                setattr(cinema, key, value)
            self.db.commit()
            self.db.refresh(cinema)
            return cinema
        return None
    
    def delete(self, cinema_id: int) -> bool:
        """Удалить кинотеатр"""
        cinema = self.get_by_id(cinema_id)
        if cinema:
            self.db.delete(cinema)
            self.db.commit()
            return True
        return False
    
    def get_by_name(self, name: str) -> Optional[CinemaModel]:
        """Найти кинотеатр по названию"""
        return self.db.query(self.cinema_model).filter(self.cinema_model.name == name).first()
    
    def get_or_create(self, cinema_data: dict) -> Tuple[CinemaModel, bool]:
        """
        Получить кинотеатр по названию или создать новый.
        Возвращает кортеж: (объект, создан ли он)
        """
        existing = self.get_by_name(cinema_data["name"])
        if existing:
            return existing, False
        
        new_cinema = self.create(cinema_data)
        return new_cinema, True 