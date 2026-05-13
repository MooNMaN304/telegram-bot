# StaffResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**staff_id** | **int** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**description** | **str** |  | 
**poster_url** | **str** |  | 
**profession_text** | **str** |  | 
**profession_key** | **str** |  | 

## Example

```python
from openapi_client.models.staff_response import StaffResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StaffResponse from a JSON string
staff_response_instance = StaffResponse.from_json(json)
# print the JSON string representation of the object
print(StaffResponse.to_json())

# convert the object into a dict
staff_response_dict = staff_response_instance.to_dict()
# create an instance of StaffResponse from a dict
staff_response_from_dict = StaffResponse.from_dict(staff_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


