# PersonByNameResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**web_url** | **str** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**sex** | **str** |  | [optional] 
**poster_url** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.person_by_name_response_items import PersonByNameResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of PersonByNameResponseItems from a JSON string
person_by_name_response_items_instance = PersonByNameResponseItems.from_json(json)
# print the JSON string representation of the object
print(PersonByNameResponseItems.to_json())

# convert the object into a dict
person_by_name_response_items_dict = person_by_name_response_items_instance.to_dict()
# create an instance of PersonByNameResponseItems from a dict
person_by_name_response_items_from_dict = PersonByNameResponseItems.from_dict(person_by_name_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


