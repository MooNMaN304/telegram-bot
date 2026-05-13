# ExternalSourceResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 
**platform** | **str** |  | [optional] 
**logo_url** | **str** |  | [optional] 
**positive_rating** | **int** |  | [optional] 
**negative_rating** | **int** |  | [optional] 
**author** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.external_source_response_items import ExternalSourceResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalSourceResponseItems from a JSON string
external_source_response_items_instance = ExternalSourceResponseItems.from_json(json)
# print the JSON string representation of the object
print(ExternalSourceResponseItems.to_json())

# convert the object into a dict
external_source_response_items_dict = external_source_response_items_instance.to_dict()
# create an instance of ExternalSourceResponseItems from a dict
external_source_response_items_from_dict = ExternalSourceResponseItems.from_dict(external_source_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


