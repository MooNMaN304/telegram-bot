from sqlalchemy import Column, String, Integer, JSON, BigInteger
from sqlalchemy.orm import relationship
from src.base.base_model import Base


class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    genre = Column(String(255))  # строка с жанрами через запятую
    description = Column(String(1500))
    poster = Column(String(255))
    additional_data = Column(JSON)  # JSON с доп. данными (name_en, duration, year, kinomax_url, kinomax_id и тд)
    kinopoisk_id = Column(BigInteger, unique=True, nullable=True)

    # Отношения
    cinema_movies = relationship("CinemaMovieModel", back_populates="movie", cascade="all, delete-orphan")
    sessions = relationship("SessionModel", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Movie(id={self.id}, name='{self.name}')"

    def __str__(self):
        sessions_count = len(self.sessions) if self.sessions else 0
        cinemas_count = len(self.cinema_movies) if self.cinema_movies else 0
        return f"Фильм '{self.name}' (кинотеатров: {cinemas_count}, сеансов: {sessions_count})"
