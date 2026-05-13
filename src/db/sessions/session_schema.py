from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from datetime import time as Time


from pydantic import BaseModel
from typing import Optional


class SessionSchema(BaseModel):
    session_id: Optional[str]  # ⬅️ ключевой момент
    date: datetime
    movie_id: Optional[int] = None
    cinema_id: Optional[int] = None
    updated_at: Optional[datetime] = None
