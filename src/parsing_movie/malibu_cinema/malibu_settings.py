from pydantic_settings import BaseSettings
from typing import Dict, ClassVar


class MaliBuSettings(BaseSettings):
    MALIBU_URL: str = "https://malibu.wikicinema.ru/"
    CINEMA_NAME: str = "Малибу"

    # -------- селекторы для главной страницы --------
    MAIN_PAGE_SELECTORS: Dict = {
        # CSS-классы типа releases-list / releases-container / releases-item
        # хэшируются Next.js/css-modules при каждом билде.
        # Используем стабильные селекторы: <main> + href-паттерн /release/
        "container_xpath": "//main",
        # Карточки ТОЛЬКО активные (без soon)
        "movie_links_xpath": ".//a[contains(@href, '/release/')]",
        # Для других функций (извлечение карточек)
        "soon_link_pattern": "soon",
        "release_link_pattern": "/release/",
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
            # Без классов — используем <main> и href-паттерн
            "container_xpath": "//main",
            "link_xpath": ".//a[contains(@href, '/release/')]",
            "release_path": "/release/",
        },
        "release_cards": {
            # Без классов — ищем все ссылки с /release/
            "card_xpath": ".//a[contains(@href, '/release/')]",
            # Вместо хэшированного класса — пробуем текстовое содержимое ссылки
            "title_xpath": ".//text()",
            "title_selector": "",
            "title_class": "",
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
