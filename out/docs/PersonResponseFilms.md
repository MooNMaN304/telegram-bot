# PersonResponseFilms


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**film_id** | **int** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**rating** | **str** |  | [optional] 
**general** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 
**profession_key** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.person_response_films import PersonResponseFilms

# TODO update the JSON string below
json = "{}"
# create an instance of PersonResponseFilms from a JSON string
person_response_films_instance = PersonResponseFilms.from_json(json)
# print the JSON string representation of the object
print(PersonResponseFilms.to_json())

# convert the object into a dict
person_response_films_dict = person_response_films_instance.to_dict()
# create an instance of PersonResponseFilms from a dict
person_response_films_from_dict = PersonResponseFilms.from_dict(person_response_films_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


