from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship
from src.base.base_model import Base


class CinemaMovieModel(Base):
    __tablename__ = "cinema_movies"
    __table_args__ = (PrimaryKeyConstraint("cinema_id", "movie_id", name="pk_cinema_movie"),)

    cinema_id = Column(Integer, ForeignKey("cinemas.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)

    # Cinema-specific данные
    cinema_movie_id = Column(String(50), nullable=True)  # ID фильма в кинотеатре (напр. 24233 на Malibu)
    cinema_movie_url = Column(String(500), nullable=True)  # URL фильма на сайте кинотеатра

    # Отношения
    cinema = relationship("CinemaModel", back_populates="cinema_movies")
    movie = relationship("MovieModel", back_populates="cinema_movies")

    def __repr__(self):
        return f"CinemaMovie(cinema_id={self.cinema_id}, movie_id={self.movie_id}, cinema_movie_id={self.cinema_movie_id})"

    def __str__(self):
        cinema_name = self.cinema.name if self.cinema else "Неизвестный кинотеатр"
        movie_name = self.movie.name if self.movie else "Неизвестный фильм"
        return f"{movie_name} в {cinema_name}"
