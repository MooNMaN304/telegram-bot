from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MalibuMovieSchema(BaseModel):
    title: str
    url: Optional[str] = None
    poster_url: Optional[str] = None
    description: Optional[str] = None
    genres: list[str] = []        # список жанров
    id_malibu: Optional[str] = None


class MalibuSessionSchema(BaseModel):
    """Схема для сеанса из кинотеатра Малибу"""
    session_id: str                # ID сеанса в кинотеатре
    date: datetime                 # дата и время сеанса
    movie_id: Optional[int] = None
    cinema_id: Optional[int] = None
    updated_at: Optional[datetime] = None