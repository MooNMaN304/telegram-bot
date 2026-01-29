# PersonResponseSpouses


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**person_id** | **int** |  | [optional] 
**name** | **str** |  | [optional] 
**divorced** | **bool** |  | [optional] 
**divorced_reason** | **str** |  | [optional] 
**sex** | **str** |  | [optional] 
**children** | **int** |  | [optional] 
**web_url** | **str** |  | [optional] 
**relation** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.person_response_spouses import PersonResponseSpouses

# TODO update the JSON string below
json = "{}"
# create an instance of PersonResponseSpouses from a JSON string
person_response_spouses_instance = PersonResponseSpouses.from_json(json)
# print the JSON string representation of the object
print(PersonResponseSpouses.to_json())

# convert the object into a dict
person_response_spouses_dict = person_response_spouses_instance.to_dict()
# create an instance of PersonResponseSpouses from a dict
person_response_spouses_from_dict = PersonResponseSpouses.from_dict(person_response_spouses_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


