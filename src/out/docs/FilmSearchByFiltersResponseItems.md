# FilmSearchByFiltersResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**imdb_id** | **str** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**name_original** | **str** |  | [optional] 
**countries** | [**List[Country]**](Country.md) |  | [optional] 
**genres** | [**List[Genre]**](Genre.md) |  | [optional] 
**rating_kinopoisk** | **float** |  | [optional] 
**rating_imdb** | **float** |  | [optional] 
**year** | **float** |  | [optional] 
**type** | **str** |  | [optional] 
**poster_url** | **str** |  | [optional] 
**poster_url_preview** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.film_search_by_filters_response_items import FilmSearchByFiltersResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of FilmSearchByFiltersResponseItems from a JSON string
film_search_by_filters_response_items_instance = FilmSearchByFiltersResponseItems.from_json(json)
# print the JSON string representation of the object
print(FilmSearchByFiltersResponseItems.to_json())

# convert the object into a dict
film_search_by_filters_response_items_dict = film_search_by_filters_response_items_instance.to_dict()
# create an instance of FilmSearchByFiltersResponseItems from a dict
film_search_by_filters_response_items_from_dict = FilmSearchByFiltersResponseItems.from_dict(film_search_by_filters_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


