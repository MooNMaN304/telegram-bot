# openapi_client.KpUsersApi

All URIs are relative to *https://kinopoiskapiunofficial.tech*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_kp_users_id_votes_get**](KpUsersApi.md#api_v1_kp_users_id_votes_get) | **GET** /api/v1/kp_users/{id}/votes | получить данные об оценках пользователя


# **api_v1_kp_users_id_votes_get**
> KinopoiskUserVoteResponse api_v1_kp_users_id_votes_get(id, page=page)

получить данные об оценках пользователя

Одна страница может содержать до 20 элементов в items. Доступны не все оценки пользователя, а примерно 1500 последних

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.kinopoisk_user_vote_response import KinopoiskUserVoteResponse
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
    api_instance = openapi_client.KpUsersApi(api_client)
    id = 56 # int | id пользователя на сайте кинопоиск
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить данные об оценках пользователя
        api_response = api_instance.api_v1_kp_users_id_votes_get(id, page=page)
        print("The response of KpUsersApi->api_v1_kp_users_id_votes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling KpUsersApi->api_v1_kp_users_id_votes_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| id пользователя на сайте кинопоиск | 
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**KinopoiskUserVoteResponse**](KinopoiskUserVoteResponse.md)

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
**429** | Слишком много запросов. Общий лимит - 2 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

