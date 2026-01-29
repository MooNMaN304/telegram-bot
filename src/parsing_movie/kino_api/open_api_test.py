"""
API Key Authentication Example.
    Given the following security scheme in the OpenAPI specification:
      components:
        securitySchemes:
          cookieAuth:         # name for the security scheme
            type: apiKey
            in: cookie
            name: JSESSIONID  # cookie name

    You can programmatically set the cookie:

conf = openapi_client.Configuration(
    api_key={'cookieAuth': 'abc123'}
    api_key_prefix={'cookieAuth': 'JSESSIONID'}
)

    The following cookie will be added to the HTTP request:
       Cookie: JSESSIONID abc123
"""

from out.openapi_client.api_client import openapi_client
from out.openapi_client.api import films_api
from out.openapi_client.configuration import Configuration
from src.settings import settings

# Настройка
config = Configuration(api_key={"ApiKeyAuth": settings.KINOPOISK_API_KEY})
# config.api_key['X-API-KEY'] = settings.KINOPOISK_API_KEY


# Использование
with openapi_client.ApiClient(config) as api_client:
    api = films_api.FilmsApi(api_client)
    dir(api)
    film = api.api_v21_films_search_by_keyword_get(keyword="Сердце")
    print(film)
