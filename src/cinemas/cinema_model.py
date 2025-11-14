from src.base.base_model import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class CinemaModel(Base):
    __tablename__ = 'cinemas'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255))
    
    # Отношения
    movies = relationship("MovieModel", back_populates="cinema", cascade="all, delete-orphan")
    sessions = relationship("SessionModel", back_populates="cinema", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"Cinema(id={self.id}, name='{self.name}', address='{self.address}')"
    
    def __str__(self):
        return f"Кинотеатр: {self.name} ({self.address})"
    

from src.sessions.session_model import SessionModel  # noqa
from src.movies.movie_model import MovieModel  # noqa