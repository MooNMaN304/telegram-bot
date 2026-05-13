from src.base.base_model import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class CinemaModel(Base):
    __tablename__ = "cinemas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255))

    # Отношения
    cinema_movies = relationship("CinemaMovieModel", back_populates="cinema", cascade="all, delete-orphan")
    sessions = relationship("SessionModel", back_populates="cinema", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Cinema(id={self.id}, name='{self.name}', address='{self.address}')"

    def __str__(self):
        movies_count = len(self.cinema_movies) if self.cinema_movies else 0
        return f"Кинотеатр: {self.name} ({self.address}) - {movies_count} фильмов"


from src.db.sessions.session_model import SessionModel  # noqa
from src.db.cinema_movie.cinema_movie_model import CinemaMovieModel  # noqa
