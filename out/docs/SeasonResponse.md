# SeasonResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[Season]**](Season.md) |  | 

## Example

```python
from openapi_client.models.season_response import SeasonResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SeasonResponse from a JSON string
season_response_instance = SeasonResponse.from_json(json)
# print the JSON string representation of the object
print(SeasonResponse.to_json())

# convert the object into a dict
season_response_dict = season_response_instance.to_dict()
# create an instance of SeasonResponse from a dict
season_response_from_dict = SeasonResponse.from_dict(season_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


