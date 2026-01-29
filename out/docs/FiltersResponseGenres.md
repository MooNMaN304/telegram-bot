# FiltersResponseGenres


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**genre** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.filters_response_genres import FiltersResponseGenres

# TODO update the JSON string below
json = "{}"
# create an instance of FiltersResponseGenres from a JSON string
filters_response_genres_instance = FiltersResponseGenres.from_json(json)
# print the JSON string representation of the object
print(FiltersResponseGenres.to_json())

# convert the object into a dict
filters_response_genres_dict = filters_response_genres_instance.to_dict()
# create an instance of FiltersResponseGenres from a dict
filters_response_genres_from_dict = FiltersResponseGenres.from_dict(filters_response_genres_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


