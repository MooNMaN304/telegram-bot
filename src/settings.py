from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    REQUEST_TIMEOUT: int = 30
    WAIT_PAGE_LOAD: int = 3
    ADMIN_TELEGRAM_ID: str
    KINOPOISK_API_KEY: str
    #KINOPOISK_BASE_URL: str
    DEEPSEEK_API_KEY: str


    # Настройки БД
    DATABASE_URL: str = "sqlite:///./cinema.db"

    # Другие настройки
    LOG_LEVEL: str = "INFO"

    HEADERS: Dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()



