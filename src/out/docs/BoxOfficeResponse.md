# BoxOfficeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[BoxOffice]**](BoxOffice.md) |  | 

## Example

```python
from openapi_client.models.box_office_response import BoxOfficeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BoxOfficeResponse from a JSON string
box_office_response_instance = BoxOfficeResponse.from_json(json)
# print the JSON string representation of the object
print(BoxOfficeResponse.to_json())

# convert the object into a dict
box_office_response_dict = box_office_response_instance.to_dict()
# create an instance of BoxOfficeResponse from a dict
box_office_response_from_dict = BoxOfficeResponse.from_dict(box_office_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


