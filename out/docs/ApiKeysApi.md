# openapi_client.ApiKeysApi

All URIs are relative to *https://kinopoiskapiunofficial.tech*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_api_keys_api_key_get**](ApiKeysApi.md#api_v1_api_keys_api_key_get) | **GET** /api/v1/api_keys/{apiKey} | получить данные об api key


# **api_v1_api_keys_api_key_get**
> ApiKeyResponse api_v1_api_keys_api_key_get(api_key)

получить данные об api key

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.api_key_response import ApiKeyResponse
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
    api_instance = openapi_client.ApiKeysApi(api_client)
    api_key = 'api_key_example' # str | api key

    try:
        # получить данные об api key
        api_response = api_instance.api_v1_api_keys_api_key_get(api_key)
        print("The response of ApiKeysApi->api_v1_api_keys_api_key_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiKeysApi->api_v1_api_keys_api_key_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_key** | **str**| api key | 

### Return type

[**ApiKeyResponse**](ApiKeyResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Запрос выполнен успешно |  -  |
**429** | Слишком много запросов. Общий лимит - 2 запросов в секунду |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

