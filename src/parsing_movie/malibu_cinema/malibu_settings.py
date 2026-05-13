from pydantic_settings import BaseSettings
from typing import Dict, ClassVar


class MaliBuSettings(BaseSettings):
    MALIBU_URL: str = "https://malibu.wikicinema.ru/"
    CINEMA_NAME: str = "Малибу"

    # -------- селекторы для главной страницы --------
      # Главная страница
    MAIN_PAGE_SELECTORS: Dict = {
        "movies_container_xpath": "//div[contains(@class, 'releases-list')]",
        "soon_container_id": "releasesSoon",
        "soon_class_part": "soon"
    }

    # Селекторы для сеансов (расписания)
    SESSION_SELECTORS: Dict = {
        "malibu": {
            # контейнер дня с расписанием
            "schedule_block": ".release-schedule__items",
            # ключевой селектор - ищем по data-атрибуту
            "seance_item_xpath": ".//div[@data-seance-id]",
            # родитель сеанса для получения времени и формата
            "seance_parent_xpath": "./ancestor::div[contains(@class, 'seance-item')]",
        }
    }

    # Опции парсинга сеансов
    SESSION_PARSING_OPTIONS: Dict = {
        "max_empty_days": 2,  # если 2 дня подряд пусто - останавливаемся
        "days_to_check": 5,  # сколько дней вперёд проверяем
    }

    # Селекторы для html_utils (чистый парсинг без Selenium)
    HTML_UTILS_SELECTORS: Dict = {
        "release_links": {
            "container_xpath": "//div[contains(@class, 'releases-list')]",
            "link_xpath": ".//a[contains(@href, '/release/')]",
            "release_path": "/release/",
        },
        "release_cards": {
            "card_xpath": ".//a[contains(@class, 'releases-item') and contains(@href, '/release/')]",
            "title_class": "releases-item-description__title",
        },
        "film_title": {
            "h1_class": "release__title",
            "general_h1_selector": ".//h1",
            "og_meta": "og:title",
            "title_tag_selector": "//title/text()",
            "title_suffix": " - кинотеатр Malibu",
        }
    }


malibu_settings = MaliBuSettings()
