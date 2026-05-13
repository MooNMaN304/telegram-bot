# ApiKeyResponseTotalQuota


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **int** |  | 
**used** | **int** |  | 

## Example

```python
from openapi_client.models.api_key_response_total_quota import ApiKeyResponseTotalQuota

# TODO update the JSON string below
json = "{}"
# create an instance of ApiKeyResponseTotalQuota from a JSON string
api_key_response_total_quota_instance = ApiKeyResponseTotalQuota.from_json(json)
# print the JSON string representation of the object
print(ApiKeyResponseTotalQuota.to_json())

# convert the object into a dict
api_key_response_total_quota_dict = api_key_response_total_quota_instance.to_dict()
# create an instance of ApiKeyResponseTotalQuota from a dict
api_key_response_total_quota_from_dict = ApiKeyResponseTotalQuota.from_dict(api_key_response_total_quota_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


