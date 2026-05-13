# openapi_client.StaffApi

All URIs are relative to *https://kinopoiskapiunofficial.tech*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_staff_get**](StaffApi.md#api_v1_staff_get) | **GET** /api/v1/staff | получить данные об актерах, режисерах и т.д. по kinopoisk film id
[**api_v1_staff_id_get**](StaffApi.md#api_v1_staff_id_get) | **GET** /api/v1/staff/{id} | получить данные о конкретном человеке по kinopoisk person id


# **api_v1_staff_get**
> List[StaffResponse] api_v1_staff_get(film_id)

получить данные об актерах, режисерах и т.д. по kinopoisk film id

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.staff_response import StaffResponse
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
    api_instance = openapi_client.StaffApi(api_client)
    film_id = 56 # int | kinopoisk film id

    try:
        # получить данные об актерах, режисерах и т.д. по kinopoisk film id
        api_response = api_instance.api_v1_staff_get(film_id)
        print("The response of StaffApi->api_v1_staff_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StaffApi->api_v1_staff_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **film_id** | **int**| kinopoisk film id | 

### Return type

[**List[StaffResponse]**](StaffResponse.md)

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
**404** | Данные не найдены |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_staff_id_get**
> PersonResponse api_v1_staff_id_get(id)

получить данные о конкретном человеке по kinopoisk person id

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.person_response import PersonResponse
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
    api_instance = openapi_client.StaffApi(api_client)
    id = 56 # int | kinopoisk person id

    try:
        # получить данные о конкретном человеке по kinopoisk person id
        api_response = api_instance.api_v1_staff_id_get(id)
        print("The response of StaffApi->api_v1_staff_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StaffApi->api_v1_staff_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| kinopoisk person id | 

### Return type

[**PersonResponse**](PersonResponse.md)

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
**404** | Данные не найдены |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

