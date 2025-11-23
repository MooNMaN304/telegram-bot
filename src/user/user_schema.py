from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Это важно!
    
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None