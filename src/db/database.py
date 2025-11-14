import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Абсолютный путь к базе
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cinema.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Создаём локальную фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Генератор сессии SQLAlchemy.
    Используется для получения сессии БД через 'next(get_db())' или в FastAPI dependency.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
