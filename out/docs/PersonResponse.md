# PersonResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**person_id** | **int** |  | 
**web_url** | **str** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**sex** | **str** |  | 
**poster_url** | **str** |  | 
**growth** | **str** |  | 
**birthday** | **str** |  | 
**death** | **str** |  | 
**age** | **int** |  | 
**birthplace** | **str** |  | 
**deathplace** | **str** |  | 
**has_awards** | **int** |  | 
**profession** | **str** |  | 
**facts** | **List[str]** |  | 
**spouses** | [**List[PersonResponseSpouses]**](PersonResponseSpouses.md) |  | 
**films** | [**List[PersonResponseFilms]**](PersonResponseFilms.md) |  | 

## Example

```python
from openapi_client.models.person_response import PersonResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PersonResponse from a JSON string
person_response_instance = PersonResponse.from_json(json)
# print the JSON string representation of the object
print(PersonResponse.to_json())

# convert the object into a dict
person_response_dict = person_response_instance.to_dict()
# create an instance of PersonResponse from a dict
person_response_from_dict = PersonResponse.from_dict(person_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


