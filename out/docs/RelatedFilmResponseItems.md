# RelatedFilmResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**name_original** | **str** |  | [optional] 
**poster_url** | **str** |  | [optional] 
**poster_url_preview** | **str** |  | [optional] 
**relation_type** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.related_film_response_items import RelatedFilmResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedFilmResponseItems from a JSON string
related_film_response_items_instance = RelatedFilmResponseItems.from_json(json)
# print the JSON string representation of the object
print(RelatedFilmResponseItems.to_json())

# convert the object into a dict
related_film_response_items_dict = related_film_response_items_instance.to_dict()
# create an instance of RelatedFilmResponseItems from a dict
related_film_response_items_from_dict = RelatedFilmResponseItems.from_dict(related_film_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


