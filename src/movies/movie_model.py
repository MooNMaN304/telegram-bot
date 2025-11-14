from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from src.base.base_model import Base

class MovieModel(Base):
    __tablename__ = 'movies'
    __table_args__ = (
        UniqueConstraint('name', 'cinema_id', name='uix_name_cinema'),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    genre = Column(String(255))        # строка с жанрами через запятую
    description = Column(String(500))
    poster = Column(String(255))
    additional_data = Column(JSON)     # JSON с доп. данными
    cinema_id = Column(Integer, ForeignKey('cinemas.id'), nullable=False)
    
    # Отношения
    cinema = relationship("CinemaModel", back_populates="movies")
    sessions = relationship("SessionModel", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Movie(id={self.id}, name='{self.name}', cinema_id={self.cinema_id})"
    
    def __str__(self):
        sessions_count = len(self.sessions) if self.sessions else 0
        cinema_name = self.cinema.name if self.cinema else "Неизвестный кинотеатр"
        return f"Фильм '{self.name}' в {cinema_name} (сеансов: {sessions_count})"
