from src.base.base_model import Base
from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    def __str__(self):
        return f"User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})"  

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"
