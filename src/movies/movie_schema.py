from pydantic import BaseModel
from typing import Optional


class BaseMovieSchema(BaseModel):    #MalibuMovieSchema
    title: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    genres: list[str] = []
    kinopoisk_id: Optional[int] = None