# ExternalSourceResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Суммарное кол-во сайтов | 
**items** | [**List[ExternalSourceResponseItems]**](ExternalSourceResponseItems.md) |  | 

## Example

```python
from openapi_client.models.external_source_response import ExternalSourceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalSourceResponse from a JSON string
external_source_response_instance = ExternalSourceResponse.from_json(json)
# print the JSON string representation of the object
print(ExternalSourceResponse.to_json())

# convert the object into a dict
external_source_response_dict = external_source_response_instance.to_dict()
# create an instance of ExternalSourceResponse from a dict
external_source_response_from_dict = ExternalSourceResponse.from_dict(external_source_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


