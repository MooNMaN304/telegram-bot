# openapi_client.FilmsApi

All URIs are relative to *https://kinopoiskapiunofficial.tech*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v21_films_id_sequels_and_prequels_get**](FilmsApi.md#api_v21_films_id_sequels_and_prequels_get) | **GET** /api/v2.1/films/{id}/sequels_and_prequels | получить сиквелы и приквелы для фильма по kinopoisk film id
[**api_v21_films_search_by_keyword_get**](FilmsApi.md#api_v21_films_search_by_keyword_get) | **GET** /api/v2.1/films/search-by-keyword | получить список фильмов по ключевым словам
[**api_v22_films_collections_get**](FilmsApi.md#api_v22_films_collections_get) | **GET** /api/v2.2/films/collections | получить список фильмов из различных топов или коллекций. Например https://www.kinopoisk.ru/top/lists/58/
[**api_v22_films_filters_get**](FilmsApi.md#api_v22_films_filters_get) | **GET** /api/v2.2/films/filters | получить id стран и жанров для использования в /api/v2.2/films
[**api_v22_films_get**](FilmsApi.md#api_v22_films_get) | **GET** /api/v2.2/films | получить список фильмов по различным фильтрам
[**api_v22_films_id_awards_get**](FilmsApi.md#api_v22_films_id_awards_get) | **GET** /api/v2.2/films/{id}/awards | получить данные о наградах фильма по kinopoisk film id
[**api_v22_films_id_box_office_get**](FilmsApi.md#api_v22_films_id_box_office_get) | **GET** /api/v2.2/films/{id}/box_office | получить данные о бюджете и сборах фильма по kinopoisk film id
[**api_v22_films_id_distributions_get**](FilmsApi.md#api_v22_films_id_distributions_get) | **GET** /api/v2.2/films/{id}/distributions | получить данные о прокате фильма по kinopoisk film id
[**api_v22_films_id_external_sources_get**](FilmsApi.md#api_v22_films_id_external_sources_get) | **GET** /api/v2.2/films/{id}/external_sources | получить список сайтов, где можно посмотреть фильм по kinopoisk film id
[**api_v22_films_id_facts_get**](FilmsApi.md#api_v22_films_id_facts_get) | **GET** /api/v2.2/films/{id}/facts | получить данные о фактах и ошибках в фильме по kinopoisk film id
[**api_v22_films_id_get**](FilmsApi.md#api_v22_films_id_get) | **GET** /api/v2.2/films/{id} | получить данные о фильме по kinopoisk id
[**api_v22_films_id_images_get**](FilmsApi.md#api_v22_films_id_images_get) | **GET** /api/v2.2/films/{id}/images | получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id
[**api_v22_films_id_relations_get**](FilmsApi.md#api_v22_films_id_relations_get) | **GET** /api/v2.2/films/{id}/relations | получить список связанных фильмов по kinopoisk film id
[**api_v22_films_id_reviews_get**](FilmsApi.md#api_v22_films_id_reviews_get) | **GET** /api/v2.2/films/{id}/reviews | получить список рецензии зрителей по kinopoisk film id
[**api_v22_films_id_seasons_get**](FilmsApi.md#api_v22_films_id_seasons_get) | **GET** /api/v2.2/films/{id}/seasons | получить данные о сезонах для сериала по kinopoisk film id
[**api_v22_films_id_similars_get**](FilmsApi.md#api_v22_films_id_similars_get) | **GET** /api/v2.2/films/{id}/similars | получить список похожих фильмов по kinopoisk film id
[**api_v22_films_id_videos_get**](FilmsApi.md#api_v22_films_id_videos_get) | **GET** /api/v2.2/films/{id}/videos | получить трейлеры,тизеры,видео для фильма по kinopoisk film id
[**api_v22_films_premieres_get**](FilmsApi.md#api_v22_films_premieres_get) | **GET** /api/v2.2/films/premieres | получить список кинопремьер


# **api_v21_films_id_sequels_and_prequels_get**
> List[FilmSequelsAndPrequelsResponse] api_v21_films_id_sequels_and_prequels_get(id)

получить сиквелы и приквелы для фильма по kinopoisk film id

tbd

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.film_sequels_and_prequels_response import FilmSequelsAndPrequelsResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить сиквелы и приквелы для фильма по kinopoisk film id
        api_response = api_instance.api_v21_films_id_sequels_and_prequels_get(id)
        print("The response of FilmsApi->api_v21_films_id_sequels_and_prequels_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v21_films_id_sequels_and_prequels_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**List[FilmSequelsAndPrequelsResponse]**](FilmSequelsAndPrequelsResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**404** | Фильм не найден |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v21_films_search_by_keyword_get**
> FilmSearchResponse api_v21_films_search_by_keyword_get(keyword, page=page)

получить список фильмов по ключевым словам

Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.film_search_response import FilmSearchResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    keyword = 'keyword_example' # str | ключивые слова для поиска
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить список фильмов по ключевым словам
        api_response = api_instance.api_v21_films_search_by_keyword_get(keyword, page=page)
        print("The response of FilmsApi->api_v21_films_search_by_keyword_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v21_films_search_by_keyword_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **keyword** | **str**| ключивые слова для поиска | 
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**FilmSearchResponse**](FilmSearchResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**404** | Фильмы не найдены |  -  |
**429** | Слишком много запросов. Лимит 5 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_collections_get**
> FilmCollectionResponse api_v22_films_collections_get(type=type, page=page)

получить список фильмов из различных топов или коллекций. Например https://www.kinopoisk.ru/top/lists/58/

Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.film_collection_response import FilmCollectionResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    type = TOP_POPULAR_ALL # str | тип топа или коллекции (optional) (default to TOP_POPULAR_ALL)
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить список фильмов из различных топов или коллекций. Например https://www.kinopoisk.ru/top/lists/58/
        api_response = api_instance.api_v22_films_collections_get(type=type, page=page)
        print("The response of FilmsApi->api_v22_films_collections_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_collections_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| тип топа или коллекции | [optional] [default to TOP_POPULAR_ALL]
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**FilmCollectionResponse**](FilmCollectionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Лимит 5 запроса в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_filters_get**
> FiltersResponse api_v22_films_filters_get()

получить id стран и жанров для использования в /api/v2.2/films

Возвращает список id стран и жанров, которые могут быть использованы в /api/v2.2/films

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.filters_response import FiltersResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)

    try:
        # получить id стран и жанров для использования в /api/v2.2/films
        api_response = api_instance.api_v22_films_filters_get()
        print("The response of FilmsApi->api_v22_films_filters_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_filters_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FiltersResponse**](FiltersResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_get**
> FilmSearchByFiltersResponse api_v22_films_get(countries=countries, genres=genres, order=order, type=type, rating_from=rating_from, rating_to=rating_to, year_from=year_from, year_to=year_to, imdb_id=imdb_id, keyword=keyword, page=page)

получить список фильмов по различным фильтрам

Возвращает список фильмов с пагинацией. Каждая страница содержит не более чем 20 фильмов. Данный эндпоинт не возращает более 400 фильмов. <i>Используй /api/v2.2/films/filters чтобы получить id стран и жанров.</i>

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.film_search_by_filters_response import FilmSearchByFiltersResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    countries = [56] # List[int] | список id стран разделенные запятой. Например <i>countries=1,2,3</i>. На данный момент можно указать не более одной страны. (optional)
    genres = [56] # List[int] | список id жанров разделенные запятой. Например <i>genres=1,2,3</i>. На данный момент можно указать не более одного жанра. (optional)
    order = RATING # str | сортировка (optional) (default to RATING)
    type = ALL # str | тип фильма (optional) (default to ALL)
    rating_from = 0 # float | минимальный рейтинг (optional) (default to 0)
    rating_to = 10 # float | максимальный рейтинг (optional) (default to 10)
    year_from = 1000 # int | минимальный год (optional) (default to 1000)
    year_to = 3000 # int | максимальный год (optional) (default to 3000)
    imdb_id = 'imdb_id_example' # str | imdb id (optional)
    keyword = 'keyword_example' # str | ключевое слово, которое встречается в названии фильма (optional)
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить список фильмов по различным фильтрам
        api_response = api_instance.api_v22_films_get(countries=countries, genres=genres, order=order, type=type, rating_from=rating_from, rating_to=rating_to, year_from=year_from, year_to=year_to, imdb_id=imdb_id, keyword=keyword, page=page)
        print("The response of FilmsApi->api_v22_films_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **countries** | [**List[int]**](int.md)| список id стран разделенные запятой. Например &lt;i&gt;countries&#x3D;1,2,3&lt;/i&gt;. На данный момент можно указать не более одной страны. | [optional] 
 **genres** | [**List[int]**](int.md)| список id жанров разделенные запятой. Например &lt;i&gt;genres&#x3D;1,2,3&lt;/i&gt;. На данный момент можно указать не более одного жанра. | [optional] 
 **order** | **str**| сортировка | [optional] [default to RATING]
 **type** | **str**| тип фильма | [optional] [default to ALL]
 **rating_from** | **float**| минимальный рейтинг | [optional] [default to 0]
 **rating_to** | **float**| максимальный рейтинг | [optional] [default to 10]
 **year_from** | **int**| минимальный год | [optional] [default to 1000]
 **year_to** | **int**| максимальный год | [optional] [default to 3000]
 **imdb_id** | **str**| imdb id | [optional] 
 **keyword** | **str**| ключевое слово, которое встречается в названии фильма | [optional] 
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**FilmSearchByFiltersResponse**](FilmSearchByFiltersResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Лимит 5 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_awards_get**
> AwardResponse api_v22_films_id_awards_get(id)

получить данные о наградах фильма по kinopoisk film id

Данный эндпоинт возвращает данные о наградах и премиях фильма.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.award_response import AwardResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить данные о наградах фильма по kinopoisk film id
        api_response = api_instance.api_v22_films_id_awards_get(id)
        print("The response of FilmsApi->api_v22_films_id_awards_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_awards_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**AwardResponse**](AwardResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_box_office_get**
> BoxOfficeResponse api_v22_films_id_box_office_get(id)

получить данные о бюджете и сборах фильма по kinopoisk film id

Данный эндпоинт возвращает данные о бюджете и сборах.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.box_office_response import BoxOfficeResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить данные о бюджете и сборах фильма по kinopoisk film id
        api_response = api_instance.api_v22_films_id_box_office_get(id)
        print("The response of FilmsApi->api_v22_films_id_box_office_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_box_office_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**BoxOfficeResponse**](BoxOfficeResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_distributions_get**
> DistributionResponse api_v22_films_id_distributions_get(id)

получить данные о прокате фильма по kinopoisk film id

Данный эндпоинт возвращает данные о прокате в разных странах.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.distribution_response import DistributionResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить данные о прокате фильма по kinopoisk film id
        api_response = api_instance.api_v22_films_id_distributions_get(id)
        print("The response of FilmsApi->api_v22_films_id_distributions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_distributions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**DistributionResponse**](DistributionResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_external_sources_get**
> ExternalSourceResponse api_v22_films_id_external_sources_get(id, page=page)

получить список сайтов, где можно посмотреть фильм по kinopoisk film id

Возвращает список сайтов с пагинацией. Каждая страница содержит не более чем 20 рецензий.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.external_source_response import ExternalSourceResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить список сайтов, где можно посмотреть фильм по kinopoisk film id
        api_response = api_instance.api_v22_films_id_external_sources_get(id, page=page)
        print("The response of FilmsApi->api_v22_films_id_external_sources_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_external_sources_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**ExternalSourceResponse**](ExternalSourceResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_facts_get**
> FactResponse api_v22_films_id_facts_get(id)

получить данные о фактах и ошибках в фильме по kinopoisk film id

Данный эндпоинт возвращает список фактов и ошибок в фильме. <br> type - <b>FACT</b>, обозначает интересный факт о фильме. <br> type - <b>BLOOPER</b>, обозначает ошибку в фильме.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.fact_response import FactResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить данные о фактах и ошибках в фильме по kinopoisk film id
        api_response = api_instance.api_v22_films_id_facts_get(id)
        print("The response of FilmsApi->api_v22_films_id_facts_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_facts_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**FactResponse**](FactResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_get**
> Film api_v22_films_id_get(id)

получить данные о фильме по kinopoisk id

Данный эндпоинт возвращает базовые данные о фильме. Поле <b>lastSync</b> показывает дату последнего обновления данных.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.film import Film
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить данные о фильме по kinopoisk id
        api_response = api_instance.api_v22_films_id_get(id)
        print("The response of FilmsApi->api_v22_films_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**Film**](Film.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**404** | Фильм не найден |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_images_get**
> ImageResponse api_v22_films_id_images_get(id, type=type, page=page)

получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id

Данный эндпоинт возвращает изображения связанные с фильмом с пагинацией. Каждая страница содержит <b>не более чем 20 фильмов</b>.</br> Доступные изображения:</br> <ul> <li>STILL - кадры</li> <li>SHOOTING - изображения со съемок</li> <li>POSTER - постеры</li> <li>FAN_ART - фан-арты</li> <li>PROMO - промо</li> <li>CONCEPT - концепт-арты</li> <li>WALLPAPER - обои</li> <li>COVER - обложки</li> <li>SCREENSHOT - скриншоты</li> </ul> 

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.image_response import ImageResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id
    type = STILL # str | тип изображения (optional) (default to STILL)
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить изображения(кадры, постеры, фан-арты, обои и т.д.) связанные с фильмом по kinopoisk film id
        api_response = api_instance.api_v22_films_id_images_get(id, type=type, page=page)
        print("The response of FilmsApi->api_v22_films_id_images_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_images_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 
 **type** | **str**| тип изображения | [optional] [default to STILL]
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**ImageResponse**](ImageResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_relations_get**
> RelatedFilmResponse api_v22_films_id_relations_get(id)

получить список связанных фильмов по kinopoisk film id

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.related_film_response import RelatedFilmResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить список связанных фильмов по kinopoisk film id
        api_response = api_instance.api_v22_films_id_relations_get(id)
        print("The response of FilmsApi->api_v22_films_id_relations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_relations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**RelatedFilmResponse**](RelatedFilmResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_reviews_get**
> ReviewResponse api_v22_films_id_reviews_get(id, page=page, order=order)

получить список рецензии зрителей по kinopoisk film id

Возвращает список рецензии зрителей с пагинацией. Каждая страница содержит не более чем 20 рецензий.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.review_response import ReviewResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id
    page = 1 # int | номер страницы (optional) (default to 1)
    order = DATE_DESC # str | тип сортировки (optional) (default to DATE_DESC)

    try:
        # получить список рецензии зрителей по kinopoisk film id
        api_response = api_instance.api_v22_films_id_reviews_get(id, page=page, order=order)
        print("The response of FilmsApi->api_v22_films_id_reviews_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_reviews_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 
 **page** | **int**| номер страницы | [optional] [default to 1]
 **order** | **str**| тип сортировки | [optional] [default to DATE_DESC]

### Return type

[**ReviewResponse**](ReviewResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_seasons_get**
> SeasonResponse api_v22_films_id_seasons_get(id)

получить данные о сезонах для сериала по kinopoisk film id

Данный эндпоинт возвращает данные о сезонах для сериала.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.season_response import SeasonResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить данные о сезонах для сериала по kinopoisk film id
        api_response = api_instance.api_v22_films_id_seasons_get(id)
        print("The response of FilmsApi->api_v22_films_id_seasons_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_seasons_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**SeasonResponse**](SeasonResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_similars_get**
> SimilarFilmResponse api_v22_films_id_similars_get(id)

получить список похожих фильмов по kinopoisk film id

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.similar_film_response import SimilarFilmResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить список похожих фильмов по kinopoisk film id
        api_response = api_instance.api_v22_films_id_similars_get(id)
        print("The response of FilmsApi->api_v22_films_id_similars_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_similars_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**SimilarFilmResponse**](SimilarFilmResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_id_videos_get**
> VideoResponse api_v22_films_id_videos_get(id)

получить трейлеры,тизеры,видео для фильма по kinopoisk film id

Данный эндпоинт возвращает трейлеры,тизеры,видео для фильма по kinopoisk film id. В данный момент доступно три site:  <br/> <ul><li>YOUTUBE - в этом случае <b>url</b> это просто ссылка на youtube видео.</li><li>YANDEX_DISK - в этом случае <b>url</b> это ссылка на yandex disk.</li><li>KINOPOISK_WIDGET - в этом случае <b>url</b> это ссылка на кинопоиск виджет. <b>Видео доступно только с РФ ip</b>. Например https://widgets.kinopoisk.ru/discovery/trailer/123573?onlyPlayer=1&autoplay=1&cover=1. Если вы хотите вставить этот виджет на вашу страницу, вы можете сделать следующее:  <br/><br/>&lt;script src=&quot;https://unpkg.com/@ungap/custom-elements-builtin&quot;&gt;&lt;/script&gt;<br/>&lt;script type=&quot;module&quot; src=&quot;https://unpkg.com/x-frame-bypass&quot;&gt;&lt;/script&gt;<br/>&lt;iframe is=&quot;x-frame-bypass&quot; src=&quot;https://widgets.kinopoisk.ru/discovery/trailer/167560?onlyPlayer=1&amp;autoplay=1&amp;cover=1&quot; width=&quot;500&quot; height=&quot;500&quot;&gt;&lt;/iframe&gt;</li></ul>

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.video_response import VideoResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    id = 56 # int | kinopoisk film id

    try:
        # получить трейлеры,тизеры,видео для фильма по kinopoisk film id
        api_response = api_instance.api_v22_films_id_videos_get(id)
        print("The response of FilmsApi->api_v22_films_id_videos_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_id_videos_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk film id | 

### Return type

[**VideoResponse**](VideoResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v22_films_premieres_get**
> PremiereResponse api_v22_films_premieres_get(year, month)

получить список кинопремьер

Данный эндпоинт возвращает список кинопремьер. Например https://www.kinopoisk.ru/premiere/

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.premiere_response import PremiereResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://kinopoiskapiunofficial.tech
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://kinopoiskapiunofficial.tech"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.FilmsApi(api_client)
    year = 56 # int | год релиза
    month = 'month_example' # str | месяц релиза

    try:
        # получить список кинопремьер
        api_response = api_instance.api_v22_films_premieres_get(year, month)
        print("The response of FilmsApi->api_v22_films_premieres_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilmsApi->api_v22_films_premieres_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**| год релиза | 
 **month** | **str**| месяц релиза | 

### Return type

[**PremiereResponse**](PremiereResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**401** | Пустой или неправильный токен |  -  |
**402** | Превышен лимит запросов(или дневной, или общий) |  -  |
**429** | Слишком много запросов. Лимит 5 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

