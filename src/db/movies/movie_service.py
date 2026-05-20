from typing import List, Optional
from datetime import date
from src.db.movies.movie_repository import MovieRepository
from src.db.sessions.session_repository import SessionRepository
from src.db.cinema_movie.cinema_movie_repository import CinemaMovieRepository


class MovieService:
    def __init__(
        self, 
        movie_repo: MovieRepository, 
        session_repo: SessionRepository,
        cinema_movie_repo: CinemaMovieRepository = None,
    ):
        self.movie_repo = movie_repo
        self.session_repo = session_repo
        self.cinema_movie_repo = cinema_movie_repo

    def get_movies_with_sessions_today(self):
        """Получить фильмы, которые идут сегодня."""
        return self.movie_repo.get_movies_with_sessions_today()

    def get_sessions_for_movie_today(self, movie_id: int):
        """Получить сеансы фильма на сегодня."""
        return self.session_repo.get_by_movie_and_date(movie_id, date.today())

    def get_movies_by_cinema_today(self, cinema_id: int, target_date: date = None):
        """
        Получить фильмы в конкретном кинотеатре, у которых есть сеансы на конкретную дату.
        Использует оптимизированный метод из cinema_movie_repository с JOIN.
        """
        if target_date is None:
            target_date = date.today()
        
        if self.cinema_movie_repo:
            # Используем оптимизированный метод с JOIN
            return self.cinema_movie_repo.get_movies_by_cinema_today(cinema_id, target_date)
        else:
            # Fallback на старый способ
            all_cinema_movies = self.movie_repo.get_movies_by_cinema(cinema_id)
            
            movies_with_sessions = []
            for movie in all_cinema_movies:
                sessions = self.session_repo.get_by_movie_and_date(movie.id, target_date)
                cinema_sessions = [s for s in sessions if s.cinema_id == cinema_id]
                if cinema_sessions:
                    movies_with_sessions.append(movie)
            
            return movies_with_sessions

    def get_cinemas_by_movie_today(self, movie_id: int, target_date: date = None):
        """
        Получить кинотеатры, где идёт фильм на конкретную дату с сеансами.
        Использует оптимизированный метод из cinema_movie_repository с JOIN.
        """
        if target_date is None:
            target_date = date.today()
        
        if self.cinema_movie_repo:
            # Используем оптимизированный метод с JOIN
            return self.cinema_movie_repo.get_cinemas_by_movie_today(movie_id, target_date)
        else:
            # Fallback на старый способ
            cinema_movie_relations = self.cinema_movie_repo.get_cinemas_by_movie(movie_id)
            
            cinemas_with_sessions = []
            for cm in cinema_movie_relations:
                sessions = self.session_repo.get_by_movie_and_date(movie_id, target_date)
                cinema_sessions = [s for s in sessions if s.cinema_id == cm.cinema_id]
                if cinema_sessions:
                    cinemas_with_sessions.append(cm.cinema)
            
            return cinemas_with_sessions
