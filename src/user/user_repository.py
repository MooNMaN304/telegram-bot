from sqlalchemy.orm import Session
from typing import Optional
from src.user.user_model import UserModel


class UserRepository:
    def __init__(self, db: Session, user_model=UserModel):
        self.db = db
        self.user_model = user_model

    def create(self, user_data: dict) -> UserModel:
        user = self.user_model(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_telegram_id(self, telegram_id: str) -> Optional[UserModel]:
        return (
            self.db.query(self.user_model)
            .filter_by(telegram_id=telegram_id)
            .first()
        )

    def update(self, telegram_id: str, update_data: dict) -> Optional[UserModel]:
        user = self.get_by_telegram_id(telegram_id)
        if not user:
            return None

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user
