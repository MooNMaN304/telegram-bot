from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    # Настройки парсинга
    MALIBU_URL: str = "https://malibu.wikicinema.ru/"
    REQUEST_TIMEOUT: int = 30
    WAIT_PAGE_LOAD: int = 3


    
    # список Telegram ID админов
    ADMIN_IDS = ['123456789']  

    # Настройки БД
    DATABASE_URL: str = "sqlite:///./cinema.db"

    # Другие настройки
    LOG_LEVEL: str = "INFO"

    # CSS селекторы для разных кинотеатров
    CINEMA_SELECTORS: Dict = {
        "malibu": ".releases-item.NH6Te:not(.releases-item_soon)",
    }

    # Селекторы для деталей фильма
    MOVIE_DETAILS_SELECTORS: Dict = {
        "malibu": {
            "description": [
            ".release__text span",
            ".release__text p",
            ".release__text div p span",
            ".release__text"
        ],
            "poster": ".release-poster img",
            "genre": ".release__genre",
            "title": ".release__title",
        }
    }

    # Селекторы для сеансов (расписания)
    SESSION_SELECTORS: Dict = {
        "malibu": {
            "schedule_block": ".release-schedule__list .release-schedule__item .release-schedule__items",
            "seance_item": ".seance-item",
            "seance_id": ".widget-overlay",
            "seance_time": ".seance-item__time.text.text--size-18",
            "seance_description": ".seance-item__description.seance-item__description--with-price",
        }
    }
    HEADERS: Dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    class Config:
        env_file = ".env"


settings = Settings()