# FilmSearchByFiltersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**total_pages** | **int** |  | 
**items** | [**List[FilmSearchByFiltersResponseItems]**](FilmSearchByFiltersResponseItems.md) |  | 

## Example

```python
from openapi_client.models.film_search_by_filters_response import FilmSearchByFiltersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FilmSearchByFiltersResponse from a JSON string
film_search_by_filters_response_instance = FilmSearchByFiltersResponse.from_json(json)
# print the JSON string representation of the object
print(FilmSearchByFiltersResponse.to_json())

# convert the object into a dict
film_search_by_filters_response_dict = film_search_by_filters_response_instance.to_dict()
# create an instance of FilmSearchByFiltersResponse from a dict
film_search_by_filters_response_from_dict = FilmSearchByFiltersResponse.from_dict(film_search_by_filters_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


