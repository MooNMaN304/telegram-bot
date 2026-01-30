from out.openapi_client.api_client import ApiClient
from out.openapi_client.api.films_api import FilmsApi
from out.openapi_client.configuration import Configuration
from src.settings import settings


class KinoAPIClient:
    def __init__(self):
        self.config = Configuration(
            api_key={"ApiKeyAuth": settings.KINOPOISK_API_KEY}
        )

    def find_movie_by_title(self, title: str):
        """
        Ищет фильм по названию и возвращает первый результат
        """
        with ApiClient(self.config) as api_client:
            api = FilmsApi(api_client)

            response = api.api_v21_films_search_by_keyword_get(
                keyword=title,
                page=1
            )

            films = response.films
            if not films:
                return None

            return films[0]
