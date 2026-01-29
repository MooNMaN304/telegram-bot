# SimilarFilmResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[SimilarFilmResponseItems]**](SimilarFilmResponseItems.md) |  | 

## Example

```python
from openapi_client.models.similar_film_response import SimilarFilmResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SimilarFilmResponse from a JSON string
similar_film_response_instance = SimilarFilmResponse.from_json(json)
# print the JSON string representation of the object
print(SimilarFilmResponse.to_json())

# convert the object into a dict
similar_film_response_dict = similar_film_response_instance.to_dict()
# create an instance of SimilarFilmResponse from a dict
similar_film_response_from_dict = SimilarFilmResponse.from_dict(similar_film_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


