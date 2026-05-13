# from src.base.base_model import Base
# from src.db.database import engine
# from src.db.cinemas.cinema_model import CinemaModel
# from src.db.movies.movie_model import MovieModel
# from src.db.sessions.session_model import SessionModel
# from src.db.user.user_model import UserModel


# def init_db() -> None:
#     """Create all SQLAlchemy tables registered in Base metadata."""
#     Base.metadata.create_all(bind=engine) # Этот код уже выполняется в alembic/env.py, так что его можно удалить из init_db

# if __name__ == "__main__":
#     print("Создание таблиц...")
#     print("DB file:", engine.url)

#     # создаем все таблицы, зарегистрированные в Base
#     init_db()
#     print("✅ Таблицы успешно созданы")
