# FilmCollectionResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**name_original** | **str** |  | [optional] 
**countries** | [**List[Country]**](Country.md) |  | [optional] 
**genres** | [**List[Genre]**](Genre.md) |  | [optional] 
**rating_kinopoisk** | **float** |  | [optional] 
**rating_imbd** | **float** |  | [optional] 
**year** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**poster_url** | **str** |  | [optional] 
**poster_url_preview** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.film_collection_response_items import FilmCollectionResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of FilmCollectionResponseItems from a JSON string
film_collection_response_items_instance = FilmCollectionResponseItems.from_json(json)
# print the JSON string representation of the object
print(FilmCollectionResponseItems.to_json())

# convert the object into a dict
film_collection_response_items_dict = film_collection_response_items_instance.to_dict()
# create an instance of FilmCollectionResponseItems from a dict
film_collection_response_items_from_dict = FilmCollectionResponseItems.from_dict(film_collection_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


