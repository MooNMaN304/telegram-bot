# FilmSearchResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**keyword** | **str** |  | 
**pages_count** | **int** |  | 
**search_films_count_result** | **int** |  | 
**films** | [**List[FilmSearchResponseFilms]**](FilmSearchResponseFilms.md) |  | 

## Example

```python
from openapi_client.models.film_search_response import FilmSearchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FilmSearchResponse from a JSON string
film_search_response_instance = FilmSearchResponse.from_json(json)
# print the JSON string representation of the object
print(FilmSearchResponse.to_json())

# convert the object into a dict
film_search_response_dict = film_search_response_instance.to_dict()
# create an instance of FilmSearchResponse from a dict
film_search_response_from_dict = FilmSearchResponse.from_dict(film_search_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


