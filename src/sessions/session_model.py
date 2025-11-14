from src.base.base_model import Base
from sqlalchemy import Column, ForeignKey, Integer, DateTime, UniqueConstraint, String
from sqlalchemy.orm import relationship
from datetime import datetime

class SessionModel(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        UniqueConstraint('session_id', 'cinema_id', name='uix_session_cinema'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, nullable=False)  # ID сеанса в кинотеатре
    date = Column(DateTime, default=datetime.utcnow)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    cinema_id = Column(Integer, ForeignKey('cinemas.id'))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    movie = relationship("MovieModel", back_populates="sessions")
    cinema = relationship("CinemaModel", back_populates="sessions")
    
    def __repr__(self):
        return f"Session(id={self.id}, session_id={self.session_id}, date={self.date}, movie_id={self.movie_id}, cinema_id={self.cinema_id})"
    
    def __str__(self):
        movie_name = self.movie.name if self.movie else "Неизвестный фильм"
        cinema_name = self.cinema.name if self.cinema else "Неизвестный кинотеатр"
        date_str = self.date.strftime("%d.%m.%Y %H:%M") if self.date else "Дата не указана"
        return f"Сеанс #{self.session_id}: {movie_name} в {cinema_name} ({date_str})"