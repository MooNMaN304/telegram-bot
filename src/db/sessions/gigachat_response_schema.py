from pydantic import BaseModel
from typing import List, Optional


class SessionTime(BaseModel):
    """Одиночный сеанс с временем и ценой"""
    time: str  # "16:25"
    price: Optional[int] = None  # 330
    format: Optional[str] = None  # "2D", "3D" и т.д.


class GigaChatScheduleResponse(BaseModel):
    """Ответ от GigaChat с расписанием сеансов"""
    sessions: List[SessionTime] = []
