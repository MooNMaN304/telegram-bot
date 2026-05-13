# FilmSearchResponseFilms


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**film_id** | **int** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**year** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**film_length** | **str** |  | [optional] 
**countries** | [**List[Country]**](Country.md) |  | [optional] 
**genres** | [**List[Genre]**](Genre.md) |  | [optional] 
**rating** | **str** |  | [optional] 
**rating_vote_count** | **int** |  | [optional] 
**poster_url** | **str** |  | [optional] 
**poster_url_preview** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.film_search_response_films import FilmSearchResponseFilms

# TODO update the JSON string below
json = "{}"
# create an instance of FilmSearchResponseFilms from a JSON string
film_search_response_films_instance = FilmSearchResponseFilms.from_json(json)
# print the JSON string representation of the object
print(FilmSearchResponseFilms.to_json())

# convert the object into a dict
film_search_response_films_dict = film_search_response_films_instance.to_dict()
# create an instance of FilmSearchResponseFilms from a dict
film_search_response_films_from_dict = FilmSearchResponseFilms.from_dict(film_search_response_films_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


