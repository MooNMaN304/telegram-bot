# openapi_client.MediaPostsApi

All URIs are relative to *https://kinopoiskapiunofficial.tech*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_media_posts_get**](MediaPostsApi.md#api_v1_media_posts_get) | **GET** /api/v1/media_posts | получить медиа новости с сайта кинопоиск


# **api_v1_media_posts_get**
> MediaPostsResponse api_v1_media_posts_get(page=page)

получить медиа новости с сайта кинопоиск

Одна страница может содержать до 20 элементов в items.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.media_posts_response import MediaPostsResponse
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
    api_instance = openapi_client.MediaPostsApi(api_client)
    page = 1 # int | номер страницы (optional) (default to 1)

    try:
        # получить медиа новости с сайта кинопоиск
        api_response = api_instance.api_v1_media_posts_get(page=page)
        print("The response of MediaPostsApi->api_v1_media_posts_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MediaPostsApi->api_v1_media_posts_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| номер страницы | [optional] [default to 1]

### Return type

[**MediaPostsResponse**](MediaPostsResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**429** | Слишком много запросов. Общий лимит - 20 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

