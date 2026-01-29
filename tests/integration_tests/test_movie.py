import random

import pytest
from sqlalchemy.orm import Session 

from src.movies.movie_model import MovieModel
from src.movies.movie_repository import MovieRepository

from src.sessions.session_model import SessionModel
 
from datetime import date

# @pytest.mark.parametrize('generate_cinemas,generate_movies', [(1,1)], indirect=True)
# def test_create_movies(generate_movies, test_session: Session):
#     movie = random.choice(generate_movies)
#     x = 1

# Тест создания фильма "Карты, деньги, два ствола"
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_specific_movie_created(create_specific_movie):
    movie = create_specific_movie

    assert movie.id is not None
    assert movie.name == "Карты, деньги, два ствола"


# Тест поиска фильма id
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_get_movie_by_id(test_session, create_specific_movie):
    repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    movie = create_specific_movie

    found = repo.get_by_id(movie.id)

    assert found is not None
    assert found.id == movie.id
    assert found.name == movie.name


# Тест поиска фильма по части названия
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_search_movie_by_name(test_session, create_specific_movie):
    repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    result = repo.search_by_name("Карты")

    assert len(result) == 1
    assert result[0].name == "Карты, деньги, два ствола"


# Тест обновления фильма
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_update_movie(test_session, create_specific_movie):
    repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    movie = create_specific_movie

    updated = repo.update(
        movie.id,
        {"genre": "Мелодрама"}
    )

    assert updated is not None
    assert updated.genre == "Мелодрама"



# Тест создания нового фильма
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_create_movie(test_session, generate_cinemas):
    repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    cinema = generate_cinemas[0]

    movie = repo.create({
        "name": "Большой куш",
        "genre": "Криминал",
        "cinema_id": cinema.id,
        "related_movies": {}
    })

    assert movie.id is not None
    assert movie.name == "Большой куш"



# Тест метода get_or_create для создания фильма
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_get_or_create_creates_movie(test_session, generate_cinemas):
    movi_repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    cinema = generate_cinemas[0]

    movie = movi_repo.get_or_create(
        name="Карты, деньги, два ствола",
        cinema_id=cinema.id,
        defaults={"genre": "Криминал"}
    )

    assert movie.id is not None
    assert movie.genre == "Криминал"


# Тест метода get_or_create для возврата существующего фильма
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_get_or_create_returns_existing(test_session, create_specific_movie):
    repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    cinema_id = create_specific_movie.cinema_id

    movie2 = repo.get_or_create(
        name="Карты, деньги, два ствола",
        cinema_id=cinema_id
    )

    assert movie2.id == create_specific_movie.id


# Тест получения фильмов с сеансами на сегодня
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_get_movies_with_sessions_today(
    test_session,
    create_specific_movie_sessions,
    create_specific_movie,
):
    movi_repo = MovieRepository(
        test_session,
        MovieModel,
        SessionModel
    )

    movies = movi_repo.get_movies_with_sessions_today()

    assert len(movies) == 1
    movie = movies[0]
    assert len(movie.sessions) >= 1
    assert any(s.date.date() == date.today() for s in movie.sessions)
    assert movie.id == create_specific_movie.id
    assert movie.name == create_specific_movie.name