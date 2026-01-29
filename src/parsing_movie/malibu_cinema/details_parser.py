import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.base.base_parser import BaseParser
from src.parsing_movie.malibu_cinema.extractor import MalibuDetailsExtractor
from src.parsing_movie.malibu_cinema.schemas import MalibuMovieSchema

logger = logging.getLogger(__name__)


class MalibuDetailsParser(BaseParser):
    """Парсинг деталей фильма Malibu"""

    def __init__(self, extractor: MalibuDetailsExtractor, driver):
        self.extractor = extractor
        self.driver = driver

    def parse_details(self, movie_url: str) -> MalibuMovieSchema | None:
        """
        Парсинг страницы фильма
        Возвращает валидированную схему или None
        """
        try:
            self.driver.get(movie_url)
            # Ждём загрузки страницы (как в рабочем коде)
            time.sleep(3)
            
            # ESC для закрытия рекламы
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            # Дополнительная задержка после закрытия рекламы
            time.sleep(2)

            # Ждем загрузки страницы
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".release__title, .release-poster"))
            )

            # Парсим данные
            raw_data = self.extractor.parse_movie_details(self.driver)
            
            # Добавляем URL и извлекаем ID
            raw_data["url"] = movie_url
            raw_data["id_malibu"] = self._extract_movie_id_from_url(movie_url)
            
            # Валидируем через схему
            return self._validate_movie_data(raw_data)

        except Exception as e:
            logger.error(f"Ошибка при парсинге деталей фильма {movie_url}: {e}")
            return None

    def _validate_movie_data(self, data: dict) -> MalibuMovieSchema | None:
        """Валидация данных фильма через Pydantic схему"""
        try:
            # Преобразуем жанр в список
            genre = data.get("genre") or ""
            genres_data = [genre] if genre else []
            
            # Создаем схему
            return MalibuMovieSchema(
                title=data.get("title") or "",
                url=data.get("url") or "",
                poster_url=data.get("poster") or "",
                description=data.get("description") or "",
                genres=genres_data,
                id_malibu=data.get("id_malibu") or ""
            )
            
        except Exception as e:
            logger.warning(f"Ошибка валидации данных фильма: {e}, данные: {data}")
            return None

    @staticmethod
    def _extract_movie_id_from_url(url: str) -> str:
        """Извлекает ID фильма из URL"""
        try:
            # Пример: https://malibu.wikicinema.ru/release/23608
            parts = url.split('/')
            return parts[-1] if parts else ""
        except Exception:
            return ""
        
# """
# OpenAPI → полноценный Python API-клиент

# 👉 если нужно ходить в API как в библиотеку

# Инструмент

# openapi-generator

# Установка
# brew install openapi-generator
# # или
# npm install @openapitools/openapi-generator-cli -g

# Генерация клиента
# openapi-generator-cli generate \
#   -i openapi.yaml \
#   -g python \
#   -o client

# Результат
# from client.api.user_api import UserApi

# api = UserApi()
# user = api.get_user_by_id(1)


# ✔ готовые HTTP-вызовы


# openapi-generator-cli \
#   --input https://kinopoiskapiunofficial.tech/documentation/api/openapi.json \
#   --output movie_models.py

# openapi-generator-cli generate 
#   -i https://kinopoiskapiunofficial.tech/documentation/api/openapi.json
#   -g python \
#   -o client

# python -m openapi-generator-cli \
#   --input https://kinopoiskapiunofficial.tech/documentation/api/openapi.json \
#   --output models.py 
  
  
# cd out
# pip install -e .
# """

# import openapi_client
# from openapi_client.api import films_api
# from openapi_client.configuration import Configuration

# # Настройка
# config = Configuration()
# config.api_key['X-API-KEY'] = 'ваш-api-ключ'

# # Использование
# with openapi_client.ApiClient(config) as api_client:
#     api = films_api.FilmsApi(api_client)
#     film = api.api_v22_films_film_id_get(film_id=301)
#     print(film)


