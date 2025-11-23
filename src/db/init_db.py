from src.base.base_model import Base
from src.db.database import engine
from src.cinemas.cinema_model import CinemaModel
from src.movies.movie_model import MovieModel
from src.sessions.session_model import SessionModel
from src.user.user_model import UserModel

if __name__ == "__main__":
    print("Создание таблиц...")
    print("DB file:", engine.url)

    # создаем все таблицы, зарегистрированные в Base
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы успешно созданы")
