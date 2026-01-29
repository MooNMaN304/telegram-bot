import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from src.base.base_model import Base

from src.cinemas.cinema_model import CinemaModel
from src.movies.movie_model import MovieModel
from src.sessions.session_model import SessionModel
from src.user.user_model import UserModel

import pytest
from sqlalchemy import MetaData

from faker import Faker

from datetime import datetime, timedelta
import uuid


# # Абсолютный путь к базе
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "test.db")
# DATABASE_URL = f"sqlite:///{DB_PATH}"

# # Создаём движок SQLAlchemy
# engine = create_engine(DATABASE_URL, echo=True, future=True)

# # Создаём локальную фабрику сессий
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстура для тестового движка
@pytest.fixture(scope="module")
def get_engine(pytestconfig) -> Engine:
    test_db_url = "sqlite:///:memory:"
    engine = create_engine(test_db_url)
    return engine


# Фикстура для создания таблиц в тестовой базе данных
@pytest.fixture(scope="module", autouse=True)
def create_test_tables(get_engine):
    """Create all database tables before running tests.
    This fixture runs automatically for the entire test module.
    """
    # Create all tables
    Base.metadata.create_all(bind=get_engine)
    yield
    # Optionally drop tables after all tests are done
    Base.metadata.drop_all(bind=get_engine)


 # Фикстура для фабрики сессий
@pytest.fixture(scope="module")
def session_factory(get_engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine
    )


# Фикстура для тестовой сессии
@pytest.fixture(scope="function")
def test_session(session_factory):
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


# Фикстура для очистки таблиц после каждого теста
@pytest.fixture(autouse=True)
def clean_tables(get_engine):
    """
    Очищает все таблицы после каждого теста.
    """
    yield  # Тест выполняется здесь

    # Очистка таблиц после теста
    metadata = MetaData()
    metadata.reflect(bind=get_engine)  # Явное указание bind

    with get_engine.connect() as connection:
        with connection.begin():  # Открываем транзакцию
            for table in reversed(metadata.sorted_tables):
                connection.execute(table.delete())


# Фикстура для генерации 3 кинотеатров
@pytest.fixture(scope="function")
def generate_cinemas(test_session, request) -> list[CinemaModel]:
    fake = Faker()
    value = request.param if hasattr(request, 'param') else None
    cinemas = []

    for _ in range(value):
        cinema = CinemaModel(
            name=fake.unique.word(),
            address=fake.address()
        )
        
        test_session.add(cinema)
        cinemas.append(cinema)
    test_session.commit()  # Перенесено за цикл для оптимизации

    return cinemas


# Фикстура для генерации фильмов для заданного кинотеатра
@pytest.fixture
def generate_movies(test_session, generate_cinemas, request) -> list[MovieModel]:
    fake = Faker()
    value = request.param if hasattr(request, 'param') else None
    movies = []

    for _ in range(value):  
        cinema = fake.random.choice(generate_cinemas)

        movie = MovieModel(
            name=fake.unique.word(),
            genre=", ".join(fake.words(nb=2)),
            description=fake.text(max_nb_chars=200),
            poster=fake.image_url(),
            additional_data={"rating": fake.random_int(min=1, max=10)},
            cinema_id=cinema.id,
            related_movies={}
        )

        test_session.add(movie)
        movies.append(movie)

        test_session.commit()
    return movies


# Фикстура для создания фильма "Карты, деньги, два ствола"
@pytest.fixture
def create_specific_movie(
    test_session,
    generate_cinemas
) -> MovieModel:
    cinema = generate_cinemas[0]  # берём первый кинотеатр

    movie = MovieModel(
        name="Карты, деньги, два ствола",
        genre="Боевик, Криминал, Комедия",
        description=(
            "Четверо приятелей накопили по 25 тысяч фунтов, "
            "чтобы один из них мог сыграть в карты с опытным шулером и "
            "матерым преступником по кличке Гарри Топор. "
            "Парень проиграл 500 тысяч, на выплату долга ему дали неделю, "
            "а в противном случае и ему, и его друзьям каждый день будут "
            "отрубать по пальцу. Ребята решают ограбить бандитов, "
            "решивших ограбить трех ботаников, выращивающих марихуану "
            "для местного наркобарона."
        ),
        poster="https://example.com/poster.jpg",
        additional_data={"rating": 9},
        cinema_id=cinema.id,
        related_movies={}
    )

    test_session.add(movie)
    test_session.commit()
    test_session.refresh(movie)

    return movie


# Создание сеансов на три дня для фильма выше сегодня, завтра и послезавтра
@pytest.fixture
def create_specific_movie_sessions(
    test_session,
    create_specific_movie,
    generate_cinemas
) -> list[SessionModel]:
    sessions = []
    cinema = generate_cinemas[0]
    movie = create_specific_movie

    base_date = datetime.utcnow().replace(
        hour=12, minute=0, second=0, microsecond=0
    )

    for days_offset in [0, 1, 2]:
        session = SessionModel(
            session_id=str(uuid.uuid4()),
            date=base_date + timedelta(days=days_offset),
            movie_id=movie.id,
            cinema_id=cinema.id,
        )

        test_session.add(session)
        sessions.append(session)

    test_session.commit()
    return sessions


# Фикстура для генерации сеансов для заданного фильма и кинотеатра
@pytest.fixture
def generate_sessions(test_session, generate_movies, request) -> list[SessionModel]:
    fake = Faker()
    sessions = []
    value = request.param

    """
    movies: list[MovieModel]
    """

    for _ in range(value):
        movie = fake.random.choice(generate_movies)

        session = SessionModel(
            session_id=fake.uuid4(),
            date=fake.date_time_between(start_date="-7d", end_date="+7d"),
            movie_id=movie.id,
            cinema_id=movie.cinema_id,
        )

        test_session.add(session)
        sessions.append(session)

        test_session.commit()


    return sessions


# Фикстура для создания n Юзеров
@pytest.fixture
def generate_users(test_session, request) -> list[UserModel]:
    fake = Faker()
    users = []
    value = request.param

    """
    users: list[UserModel]
    """

    for _ in range(value):
        user = UserModel(
            telegram_id=fake.uuid4(),
            username=fake.unique.word(),
            first_name=fake.unique.word(),
            last_name=fake.unique.word(),
        )

        test_session.add(user)
        users.append(user)

        test_session.commit()
    return users



