from pydantic_settings import BaseSettings
from typing import Dict


class MaliBuSettings(BaseSettings):
    MALIBU_URL: str = "https://malibu.wikicinema.ru/"

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


malibu_settings = MaliBuSettings()