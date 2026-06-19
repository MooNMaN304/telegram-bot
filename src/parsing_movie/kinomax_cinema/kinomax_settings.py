from typing import ClassVar
from pydantic_settings import BaseSettings
from typing import Dict


class KinomaxSettings(BaseSettings):
    # -------- базовый URL --------
    KINOMAX_URL: str = "https://kinomax.ru/"

    # -------- модалка выбора города --------
    CITY_MODAL: Dict = {
        "no_button_text": "Нет, другой",
        "city_button_tag": "button",
    }

    # -------- селекторы --------
    MAIN_PAGE_SELECTORS: Dict = {
        "movies_container": "npMqImZNgZWHXcs5869n",
        "movie_card": "Z4IP_eYWwdD_cOsOJsKJ",
        "movie_title_xpath": ".//div[@class='s_cU8wZmU4_RRklOdW9z']/h4/span",
    }

    # -------- XPath селекторы для парсинга главной страницы --------
    MAIN_PAGE_XPATHS: ClassVar[dict[str, str]] = {
        # 🔥 главный контейнер фильмов (вторая секция)
        "movies_section": "(//section)[2]",

        # ссылки на фильмы внутри контейнера
        "movie_links": ".//a[contains(@href, '/films/')]",

        # цепочка fallback для извлечения названия фильма
        "title_primary": ".//h4//span/text()",
        "title_fallback_1": ".//h4/text()",
        "title_fallback_2": ".//img/@alt",
    }

    CITY_SELECTORS: Dict = {
        "no_button_xpath": "//button[.//span[contains(text(), '{text}')]]",
        "city_button_xpath": "//button[normalize-space()='{city}']",
    }

    # -------- страница сеансов --------
    SESSION_SELECTORS: ClassVar[dict[str, str]] = {
        # Ждём появления хоть одного заказа (ссылка на /order/)
        "order_link_xpath": "//a[contains(@href, '/order/')]",
    }

    # -------- сообщения об отсутствии сеансов --------
    EMPTY_SCHEDULE_MESSAGES: ClassVar[list[str]] = [
        "Сеансы не найдены",
        "Расписание составляется",
    ]


    # -------- retry при капче --------
    CAPTCHA_MAX_RETRIES: int = 2
    CAPTCHA_WAIT_BEFORE_RETRY: int = 5  # секунд перед повторной попыткой

    # -------- скриншоты --------
    SCREENSHOT_AREAS: Dict = {
        "sessions": {
            # ⚠️ временные значения, потом подберём точно
            "x": 0,
            "y": 250,
            "width": 1920,
            "height": 600,
        }
    }


kinomax_settings = KinomaxSettings()
