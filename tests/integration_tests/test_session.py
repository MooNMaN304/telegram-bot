import pytest

from src.sessions.session_model import SessionModel


# Тест генерации сеансов фильма
@pytest.mark.parametrize(
    'generate_cinemas,generate_movies,generate_sessions',
    [(1, 2, 4)],
    indirect=True
)
def test_sessions_generation(generate_sessions):
    sessions = generate_sessions

    assert len(sessions) == 4

    for session in sessions:
        assert session.id is not None
        assert session.movie_id is not None
        assert session.cinema_id is not None
        assert session.date is not None