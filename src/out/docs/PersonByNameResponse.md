# PersonByNameResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[PersonByNameResponseItems]**](PersonByNameResponseItems.md) |  | 

## Example

```python
from openapi_client.models.person_by_name_response import PersonByNameResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PersonByNameResponse from a JSON string
person_by_name_response_instance = PersonByNameResponse.from_json(json)
# print the JSON string representation of the object
print(PersonByNameResponse.to_json())

# convert the object into a dict
person_by_name_response_dict = person_by_name_response_instance.to_dict()
# create an instance of PersonByNameResponse from a dict
person_by_name_response_from_dict = PersonByNameResponse.from_dict(person_by_name_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


