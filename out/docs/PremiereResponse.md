# PremiereResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[PremiereResponseItem]**](PremiereResponseItem.md) |  | 

## Example

```python
from openapi_client.models.premiere_response import PremiereResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PremiereResponse from a JSON string
premiere_response_instance = PremiereResponse.from_json(json)
# print the JSON string representation of the object
print(PremiereResponse.to_json())

# convert the object into a dict
premiere_response_dict = premiere_response_instance.to_dict()
# create an instance of PremiereResponse from a dict
premiere_response_from_dict = PremiereResponse.from_dict(premiere_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


