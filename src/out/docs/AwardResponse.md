# AwardResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[Award]**](Award.md) |  | 

## Example

```python
from openapi_client.models.award_response import AwardResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AwardResponse from a JSON string
award_response_instance = AwardResponse.from_json(json)
# print the JSON string representation of the object
print(AwardResponse.to_json())

# convert the object into a dict
award_response_dict = award_response_instance.to_dict()
# create an instance of AwardResponse from a dict
award_response_from_dict = AwardResponse.from_dict(award_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


