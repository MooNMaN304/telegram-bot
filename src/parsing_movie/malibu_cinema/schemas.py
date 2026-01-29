from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from datetime import time as Time


class MalibuMovieSchema(BaseModel):
    title: str
    url: Optional[str] = None
    poster_url: Optional[str] = None
    description: Optional[str] = None
    genres: list[str] = []        # список жанров
    id_malibu: Optional[str] = None
    kinopoisk_id: Optional[int] = None


class MalibuSessionSchema(BaseModel):
    """Схема для сеанса из кинотеатра Малибу"""
    session_id: str                # ID сеанса в кинотеатре
    date: datetime                 # дата и время сеанса
    movie_id: Optional[int] = None
    cinema_id: Optional[int] = None
    updated_at: Optional[datetime] = None

class KinomaxSessionShema(BaseModel):
    """Схема для валидации данных от гигачата сеанса из кинотеатра Киномакс"""
    
    time: Time
    price: int
    format: str  # 2D or 3D format
    @field_validator('format')
    @classmethod
    def validate_format(cls, v):
        if v not in ['2D', '3D']:
            raise ValueError('format must be either "2D" or "3D"')
        return v
    
class KinomaxSessionsShema(BaseModel):
    """Схема валидации нескольких сессия спарсенных Гигачатом"""

    sessions: list[KinomaxSessionShema] = []    