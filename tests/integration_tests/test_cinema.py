import pytest

from src.cinemas.cinema_model import CinemaModel
from src.cinemas.cinema_repository import CinemaRepository


# Тест генерации кинотеатровa
@pytest.mark.parametrize('generate_cinemas', [3], indirect=True)
def test_cinemas_generation(generate_cinemas):

    cinemas = generate_cinemas
    assert len(cinemas) == 3
    for cinema in cinemas:
        assert cinema.id is not None
        assert cinema.name is not None


# Тест создания кинотеатра
def test_create_cinema(test_session):
    repo = CinemaRepository(test_session, CinemaModel)

    cinema = repo.create({
        "name": "Cinema Unique Name",
        "address": "Some address"
    })

    assert cinema.id is not None
    assert cinema.name == "Cinema Unique Name"
