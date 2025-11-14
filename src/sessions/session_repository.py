from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from .session_model import SessionModel


class SessionRepository:
    """Репозиторий для работы с таблицей сеансов"""

    def __init__(self, db: Session, session_model: type[SessionModel]):
        self.db = db
        self.session_model = session_model

    def get_all(self) -> List[SessionModel]:
        """Получить все сеансы"""
        return self.db.query(self.session_model).all()

    def get_by_id(self, id_: int) -> Optional[SessionModel]:
        """Получить сеанс по внутреннему ID"""
        return self.db.query(self.session_model).filter(self.session_model.id == id_).first()

    def get_by_session_id(self, session_id: str, cinema_id: int) -> Optional[SessionModel]:
        """Получить сеанс по session_id (строка) и cinema_id"""
        return (
            self.db.query(self.session_model)
            .filter(
                self.session_model.session_id == session_id,
                self.session_model.cinema_id == cinema_id,
            )
            .first()
        )

    def create(self, session_data: dict) -> SessionModel:
        """Создать новый сеанс"""
        session = self.session_model(**session_data)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_or_create(self, session_id: str, cinema_id: int, defaults: dict) -> Tuple[SessionModel, bool]:
        """Получить или создать сеанс (session_id — строка)"""
        existing = self.get_by_session_id(session_id, cinema_id)
        if existing:
            return existing, False

        session_data = {
            "session_id": session_id,
            "cinema_id": cinema_id,
            **defaults,
        }
        new_session = self.session_model(**session_data)
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)
        return new_session, True

    def update(self, id_: int, update_data: dict) -> Optional[SessionModel]:
        """Обновить сеанс по внутреннему ID"""
        session = self.get_by_id(id_)
        if not session:
            return None

        for key, value in update_data.items():
            setattr(session, key, value)
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete(self, id_: int) -> bool:
        """Удалить сеанс по внутреннему ID"""
        session = self.get_by_id(id_)
        if not session:
            return False

        self.db.delete(session)
        self.db.commit()
        return True

    def get_by_movie(self, movie_id: int) -> List[SessionModel]:
        """Получить все сеансы по фильму"""
        return (
            self.db.query(self.session_model)
            .filter(self.session_model.movie_id == movie_id)
            .all()
        )

    def get_by_cinema(self, cinema_id: int) -> List[SessionModel]:
        """Получить все сеансы по кинотеатру"""
        return (
            self.db.query(self.session_model)
            .filter(self.session_model.cinema_id == cinema_id)
            .all()
        )
