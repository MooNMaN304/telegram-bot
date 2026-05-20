import pytest
from src.db.movies.movie_service import MovieService
from src.db.movies.movie_repository import MovieRepository
from src.db.sessions.session_repository import SessionRepository
from src.db.cinemas.cinema_repository import CinemaRepository
from src.db.cinema_movie.cinema_movie_repository import CinemaMovieRepository
from src.db.movies.movie_model import MovieModel
from src.db.sessions.session_model import SessionModel
from src.db.cinemas.cinema_model import CinemaModel
from src.db.cinema_movie.cinema_movie_model import CinemaMovieModel

class TestMovieService:
    @pytest.fixture
    def movie_service(self, test_session):
        movie_repo = MovieRepository(
            session=test_session,
            movie_model=MovieModel,
            session_model=SessionModel,
            cinema_movie_model=CinemaMovieModel
        )
        session_repo = SessionRepository(
            session=test_session,
            session_model=SessionModel
        )
        cinema_movie_repo = CinemaMovieRepository(
            session=test_session,
            cinema_movie_model=CinemaMovieModel
        )
        return MovieService(
            movie_repo=movie_repo,
            session_repo=session_repo,
            cinema_movie_repo=cinema_movie_repo
        )

    @pytest.mark.parametrize("generate_cinemas", [2], indirect=True)
    def test_get_all_cinemas(self, movie_service, test_session, generate_cinemas):
        cinema_repo = CinemaRepository(
            session=test_session,
            cinema_model=CinemaModel
        )
        cinemas = cinema_repo.get_all()
        assert len(cinemas) == 2
        assert cinemas[0].name in [c.name for c in generate_cinemas]

    @pytest.mark.parametrize("generate_cinemas", [1], indirect=True)
    @pytest.mark.parametrize("generate_movies", [3], indirect=True)
    def test_get_movies_by_cinema(self, movie_service, generate_cinemas, generate_movies):
        cinema = generate_cinemas[0]
        movies = movie_service.movie_repo.get_movies_by_cinema(cinema.id)
        assert len(movies) == 3
        for movie in movies:
            assert isinstance(movie, MovieModel)

    @pytest.mark.parametrize("generate_cinemas", [1], indirect=True)
    def test_get_sessions_for_movie_today(self, movie_service, generate_cinemas, create_specific_movie_sessions):
        # create_specific_movie_sessions создает сеансы на сегодня, завтра и послезавтра
        movie_id = create_specific_movie_sessions[0].movie_id
        sessions = movie_service.get_sessions_for_movie_today(movie_id)
        
        assert len(sessions) == 1
        assert sessions[0].movie_id == movie_id
        # Проверяем, что дата сеанса соответствует сегодняшнему числу
        from datetime import date
        assert sessions[0].date.date() == date.today()

    @pytest.mark.parametrize("generate_cinemas", [1], indirect=True)
    def test_get_cinema_by_id(self, test_session, generate_cinemas):
        cinema_repo = CinemaRepository(
            session=test_session,
            cinema_model=CinemaModel
        )
        cinema = generate_cinemas[0]
        found_cinema = cinema_repo.get_by_id(cinema.id)
        assert found_cinema is not None
        assert found_cinema.id == cinema.id
        assert found_cinema.name == cinema.name
