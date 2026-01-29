# SimilarFilmResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**film_id** | **int** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**name_original** | **str** |  | [optional] 
**poster_url** | **str** |  | [optional] 
**poster_url_preview** | **str** |  | [optional] 
**relation_type** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.similar_film_response_items import SimilarFilmResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of SimilarFilmResponseItems from a JSON string
similar_film_response_items_instance = SimilarFilmResponseItems.from_json(json)
# print the JSON string representation of the object
print(SimilarFilmResponseItems.to_json())

# convert the object into a dict
similar_film_response_items_dict = similar_film_response_items_instance.to_dict()
# create an instance of SimilarFilmResponseItems from a dict
similar_film_response_items_from_dict = SimilarFilmResponseItems.from_dict(similar_film_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


